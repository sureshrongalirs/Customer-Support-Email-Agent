"""Sample Knowledge Base Documents for FAISS"""

SAMPLE_DOCUMENTS = [
    {
        "id": 1,
        "title": "Account Login Issues",
        "category": "technical_support",
        "content": """
        LOGIN AND PASSWORD TROUBLESHOOTING

        Problem: Unable to login to account
        Solution:
        1. Clear your browser cache and cookies
        2. Try the 'Forgot Password' link to reset your password
        3. Ensure you are using the correct email address associated with your account
        4. Try logging in using an incognito or private browsing window
        5. If you still cannot login, our support team can help reset your account

        Problem: Password reset email not received
        Solution:
        1. Check your email spam or junk folder
        2. Wait 5-10 minutes for the email to arrive
        3. Try requesting a new password reset
        4. Verify the email address is correct in your account
        5. Contact support if you continue to have issues

        Problem: Account locked after failed login attempts
        Solution:
        1. Your account is temporarily locked for security
        2. Wait 30 minutes before trying again
        3. Try resetting your password if locked
        4. Contact support to manually unlock your account
        """,
    },
    {
        "id": 2,
        "title": "Billing and Payment Issues",
        "category": "billing",
        "content": """
        BILLING AND PAYMENT TROUBLESHOOTING

        Problem: Payment declined
        Solution:
        1. Verify your credit card details are correct
        2. Check the card expiration date has not passed
        3. Ensure you have sufficient funds
        4. Contact your bank to check for transaction blocks
        5. Try a different payment method
        6. Ensure your billing address matches your bank records

        Problem: Duplicate charges on account
        Solution:
        1. Review your transaction history in the billing section
        2. Check if charges are from different dates (not duplicates)
        3. Allow 3-5 business days for pending charges to clear
        4. If duplicate charge confirmed, contact billing support immediately
        5. We will investigate and issue a refund if needed

        Problem: Refund request
        Solution:
        1. Refunds are available within 30 days of purchase
        2. Log into your account and request a refund in the billing section
        3. Provide reason for refund request
        4. Refunds are typically processed within 5-7 business days
        5. Contact billing support for expedited refund processing

        Problem: Subscription cancellation
        Solution:
        1. You can cancel your subscription anytime in account settings
        2. Cancellation takes effect at end of current billing period
        3. You will retain access until the end of your billing cycle
        4. You can reactivate your subscription at any time
        5. Contact support if you need immediate cancellation
        """,
    },
    {
        "id": 3,
        "title": "Technical Support and Errors",
        "category": "technical_support",
        "content": """
        TECHNICAL SUPPORT AND ERROR TROUBLESHOOTING

        Problem: Slow application performance
        Solution:
        1. Check your internet connection speed
        2. Clear your browser cache and cookies
        3. Close unnecessary browser tabs and applications
        4. Disable browser extensions that might slow down the site
        5. Try using a different browser
        6. Restart your computer if issues persist

        Problem: Page not loading or timeout errors
        Solution:
        1. Refresh the page (Ctrl+R or Cmd+R)
        2. Clear browser cache and cookies
        3. Check your internet connection
        4. Disable VPN or proxy if you are using one
        5. Try accessing the site from a different network
        6. Contact support if the issue continues

        Problem: Data synchronization issues
        Solution:
        1. Log out and log back in
        2. Clear cache and refresh the page
        3. Try accessing from a different device
        4. Check your internet connection
        5. Wait a few minutes for automatic synchronization
        6. Contact support if data doesn't sync after 24 hours

        Problem: Mobile app crashes
        Solution:
        1. Update the app to the latest version
        2. Clear the app cache (Settings > Apps > Clear Cache)
        3. Uninstall and reinstall the application
        4. Ensure you have enough storage space on your device
        5. Check that your device OS is up to date
        6. Contact support with details about when the crash occurs
        """,
    },
    {
        "id": 4,
        "title": "Feature Usage Guide",
        "category": "general_inquiry",
        "content": """
        FEATURE USAGE GUIDE

        Feature: Dashboard Overview
        Description:
        - The dashboard provides a quick overview of your account
        - View recent activity and important updates
        - Access quick links to commonly used features
        - Customize your dashboard by selecting which widgets to display

        Feature: Data Export
        Description:
        - Export your data in CSV, JSON, or Excel formats
        - Use the export feature to backup your information
        - Exports are ready for download immediately
        - You can schedule automatic weekly or monthly exports

        Feature: Report Generation
        Description:
        - Generate custom reports for specific date ranges
        - Choose from pre-built report templates
        - Export reports in multiple formats
        - Schedule automated report delivery

        Feature: Notifications and Alerts
        Description:
        - Customize your notification preferences
        - Choose how you want to be notified (email, SMS, in-app)
        - Set notification frequency and types
        - Enable/disable specific alerts in your settings

        Feature: User Management
        Description:
        - Add team members to your account
        - Assign specific roles and permissions
        - Control what features each user can access
        - Remove users or change their permissions anytime
        """,
    },
    {
        "id": 5,
        "title": "Security and Privacy",
        "category": "general_inquiry",
        "content": """
        SECURITY AND PRIVACY INFORMATION

        Two-Factor Authentication (2FA)
        - Adds extra security to your account
        - You can enable 2FA in account settings
        - Choose authentication method: SMS, email, or authenticator app
        - If you lose access to your 2FA device, contact support

        Data Privacy and Protection
        - Your data is encrypted in transit and at rest
        - We comply with GDPR, CCPA, and other privacy regulations
        - You can request your data at any time
        - You can delete your account and all associated data

        Password Security Best Practices
        - Use a strong password with at least 12 characters
        - Include uppercase, lowercase, numbers, and symbols
        - Never share your password with anyone
        - Change your password regularly (every 90 days)
        - Never use the same password across multiple services

        Session Security
        - Sessions automatically expire after 30 minutes of inactivity
        - You can manually logout anytime
        - Multiple simultaneous logins are not allowed for security
        - All login attempts are logged for security auditing

        Reporting Security Issues
        - If you suspect unauthorized access, change your password immediately
        - Contact security@company.com for security concerns
        - Do not share security vulnerabilities publicly
        - Report suspected account compromise within 24 hours
        """,
    },
    {
        "id": 6,
        "title": "Account Settings and Preferences",
        "category": "general_inquiry",
        "content": """
        ACCOUNT SETTINGS AND PREFERENCES GUIDE

        Profile Settings
        - Update your name, email, and profile picture
        - Add a phone number for two-factor authentication
        - Set your preferred language and timezone
        - Update your billing address

        Email Preferences
        - Choose what emails you want to receive
        - Set email frequency (daily, weekly, or monthly)
        - Unsubscribe from specific email types
        - Manage notification settings

        Privacy Settings
        - Control who can view your profile
        - Set your profile visibility (public, private, or custom)
        - Manage who can contact you
        - Block or report users

        Connected Devices
        - View all devices logged into your account
        - Logout from specific devices remotely
        - Set device-specific security permissions
        - Monitor login history for security

        API Keys and Integrations
        - Generate API keys for integrations
        - Revoke API keys when no longer needed
        - Set API key permissions (read, write, delete)
        - View API key usage statistics

        Data and Privacy
        - Download all your account data
        - Request GDPR data export
        - Delete your account permanently
        - View your data retention settings
        """,
    },
    {
        "id": 7,
        "title": "Common Error Codes",
        "category": "technical_support",
        "content": """
        COMMON ERROR CODES AND SOLUTIONS

        Error 404 - Not Found
        Cause: The requested page or resource does not exist
        Solution:
        1. Check the URL for typos
        2. Go back to home page and navigate again
        3. Try clearing browser cache
        4. Contact support if the error persists

        Error 500 - Internal Server Error
        Cause: A server-side error occurred
        Solution:
        1. Wait a few minutes and try again
        2. Refresh the page
        3. Try again in a different browser
        4. Check system status page for outages
        5. Contact support if issue continues

        Error 403 - Forbidden/Access Denied
        Cause: You don't have permission to access this resource
        Solution:
        1. Ensure you are logged in
        2. Check your account permissions
        3. Verify you have the right subscription plan
        4. Contact support to request access

        Error 401 - Unauthorized
        Cause: Authentication failed
        Solution:
        1. Log out and log back in
        2. Verify your credentials are correct
        3. Clear browser cookies
        4. Contact support if you still cannot login

        Error 429 - Too Many Requests
        Cause: Rate limit exceeded
        Solution:
        1. Wait a few minutes before trying again
        2. Do not make multiple requests in quick succession
        3. Contact support about rate limit increase
        """,
    },
    {
        "id": 8,
        "title": "Getting Started Guide",
        "category": "general_inquiry",
        "content": """
        GETTING STARTED GUIDE FOR NEW USERS

        Step 1: Create Your Account
        - Visit the signup page
        - Enter your email and create a strong password
        - Verify your email address
        - Complete your profile information

        Step 2: Setup Your Workspace
        - Choose your workspace name
        - Select your industry/use case
        - Set your timezone and language
        - Invite team members (optional)

        Step 3: Configure Your Settings
        - Set notification preferences
        - Configure billing information
        - Enable two-factor authentication
        - Upload your company logo

        Step 4: Explore Key Features
        - Visit the dashboard
        - Explore the analytics section
        - Review available integrations
        - Check out help documentation

        Step 5: Get Support
        - Check the FAQ section
        - Contact support via email or chat
        - Schedule a demo with our team
        - Join our community forum

        Onboarding Best Practices
        - Take the interactive tutorial
        - Watch our video guides
        - Review best practices documentation
        - Join webinars for training
        """,
    },
    {
        "id": 9,
        "title": "API Integration Guide",
        "category": "technical_support",
        "content": """
        API INTEGRATION AND DOCUMENTATION

        Getting Started with API
        - Generate API key in account settings
        - API base URL: https://api.company.com/v1
        - All requests require authentication header
        - API responses are in JSON format

        Authentication
        - Include API key in Authorization header
        - Format: Authorization: Bearer YOUR_API_KEY
        - API keys have read, write, and delete permissions
        - Rotate API keys regularly for security

        Common API Endpoints
        - GET /users - Retrieve user information
        - POST /data - Create new data entry
        - PUT /data/{id} - Update existing data
        - DELETE /data/{id} - Delete data entry

        Error Handling
        - Check HTTP status codes in response
        - Handle rate limiting (429 status)
        - Implement retry logic with exponential backoff
        - Log all API errors for debugging

        Rate Limiting
        - Standard plan: 100 requests per minute
        - Professional plan: 500 requests per minute
        - Enterprise plan: Unlimited requests
        - Contact support for rate limit increase

        Example Request
        curl -X GET https://api.company.com/v1/users \\
          -H "Authorization: Bearer YOUR_API_KEY" \\
          -H "Content-Type: application/json"
        """,
    },
    {
        "id": 10,
        "title": "System Status and Maintenance",
        "category": "general_inquiry",
        "content": """
        SYSTEM STATUS AND MAINTENANCE INFORMATION

        Checking System Status
        - Visit status.company.com for real-time status
        - Subscribe to status updates via email
        - Get notifications on Twitter @company_status
        - Check service health dashboard

        Scheduled Maintenance Windows
        - We perform maintenance on Sundays 2-4 AM UTC
        - Advance notice is given for major maintenance
        - Critical data is always backed up
        - You will receive email notification before maintenance

        Service Uptime Guarantee
        - We maintain 99.9% uptime SLA
        - If downtime exceeds SLA, credits will be issued
        - Business plan customers get higher priority support
        - Enterprise customers have dedicated support

        How We Handle Outages
        - We have redundant systems in multiple regions
        - Automatic failover if primary system fails
        - Continuous monitoring 24/7
        - Incident response team available immediately

        Backup and Recovery
        - Automatic daily backups of all data
        - Weekly backup verification
        - 30-day backup retention
        - Recovery time objective (RTO): 2 hours
        - Recovery point objective (RPO): 1 hour
        """,
    },
]


def get_documents() -> list[dict]:
    """Get all sample documents.

    Returns:
        List of sample documents
    """
    return SAMPLE_DOCUMENTS


def get_documents_by_category(category: str) -> list[dict]:
    """Get documents filtered by category.

    Args:
        category: Document category

    Returns:
        List of documents in category
    """
    return [doc for doc in SAMPLE_DOCUMENTS if doc.get("category") == category]


def get_document_by_id(doc_id: int) -> dict | None:
    """Get document by ID.

    Args:
        doc_id: Document ID

    Returns:
        Document or None if not found
    """
    for doc in SAMPLE_DOCUMENTS:
        if doc.get("id") == doc_id:
            return doc
    return None