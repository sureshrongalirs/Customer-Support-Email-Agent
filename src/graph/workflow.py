"""LangGraph Workflow Definition for Email Processing"""

from typing import Any, TypedDict

from langgraph.graph import StateGraph, END

from src.core.logger import setup_logger

logger = setup_logger(__name__)


class EmailProcessingState(TypedDict):
    """State management for email processing workflow."""

    email_id: str
    sender: str
    subject: str
    body: str
    classification: dict
    extracted_entities: dict
    knowledge_base_results: dict
    draft_response: str
    requires_human_review: bool
    priority: str
    final_response: str
    sent: bool
    follow_up_scheduled: bool
    error: str | None


def create_workflow():
    """Create LangGraph workflow for email processing.

    Returns:
        Compiled StateGraph workflow
    """
    logger.info("Creating email processing workflow")

    # Lazy import nodes to avoid heavy dependencies at startup
    from src.nodes.email_processor import EmailProcessor
    from src.nodes.intent_classifier import IntentClassifier
    from src.nodes.knowledge_base_search import KnowledgeBaseSearch
    from src.nodes.response_generator import ResponseGenerator
    from src.nodes.human_review_router import HumanReviewRouter
    from src.nodes.email_sender import EmailSender
    from src.nodes.followup_scheduler import FollowupScheduler

    workflow = StateGraph(EmailProcessingState)

    email_processor = EmailProcessor()
    intent_classifier = IntentClassifier()
    kb_search = KnowledgeBaseSearch()
    response_gen = ResponseGenerator()
    human_router = HumanReviewRouter()
    email_sender = EmailSender()
    followup_scheduler = FollowupScheduler()

    workflow.add_node("parse_email", email_processor.parse)
    workflow.add_node("classify_intent", intent_classifier.classify)
    workflow.add_node("search_knowledge_base", kb_search.search)
    workflow.add_node("generate_response", response_gen.generate)
    workflow.add_node("human_review_router", human_router.route)
    workflow.add_node("send_email", email_sender.send)
    workflow.add_node("schedule_followup", followup_scheduler.schedule)

    workflow.set_entry_point("parse_email")

    workflow.add_edge("parse_email", "classify_intent")
    workflow.add_edge("classify_intent", "search_knowledge_base")
    workflow.add_edge("search_knowledge_base", "generate_response")
    workflow.add_edge("generate_response", "human_review_router")

    workflow.add_conditional_edges(
        "human_review_router",
        lambda state: "needs_review" if state.get("requires_human_review") else "ready_to_send",
        {
            "needs_review": END,
            "ready_to_send": "send_email",
        },
    )

    workflow.add_edge("send_email", "schedule_followup")
    workflow.add_edge("schedule_followup", END)

    logger.info("Workflow created successfully")
    return workflow.compile()


async def execute_workflow(state: EmailProcessingState) -> EmailProcessingState:
    """Execute email processing workflow.

    Args:
        state: Email processing state

    Returns:
        Updated workflow state
    """
    logger.info(f"Executing workflow for email: {state.get('email_id')}")

    workflow = create_workflow()
    result = await workflow.ainvoke(state)

    return result
