# Web UI Guide

## Overview

The Customer Support Email Agent includes a modern web interface for testing the system and monitoring processed emails.

## Features

✅ **Test Email Form** - Send mock emails to test the agent
✅ **Inbox View** - View all processed emails
✅ **Email Details** - View complete email and agent response
✅ **Real-time Statistics** - Monitor email processing metrics
✅ **Quick Templates** - Pre-filled test emails for common scenarios
✅ **Filtering** - Filter emails by status and category
✅ **Responsive Design** - Works on desktop, tablet, and mobile

## Accessing the UI

### Start the Server

```bash
uvicorn src.main:app --reload
```

### Open the Interface

Navigate to: **http://localhost:8000**

The UI will load automatically!

## Interface Overview

### Header

- **Title**: Customer Support Email Agent
- **Subtitle**: Test and monitor your AI-powered email responses
- **Navigation Tabs**: Test Email and Inbox

### Tab 1: Test Email

This tab allows you to send mock emails to test the agent.

#### Form Fields

1. **From Email Address**
   - Your test customer email
   - Default: `customer@example.com`
   - Must be a valid email format

2. **Subject**
   - Email subject line
   - Default: "I cannot login to my account"
   - Examples: "I was charged twice", "App keeps crashing"

3. **Message Body**
   - Email content
   - Default: "I've tried resetting my password but I'm not receiving the email. Can someone help me?"
   - Should describe the customer's issue

#### Quick Templates

Pre-filled test email templates:

1. **Login Issue**
   - Subject: "I cannot login to my account"
   - Body: Password reset troubleshooting

2. **Billing Issue**
   - Subject: "I was charged twice for my subscription"
   - Body: Duplicate charge complaint

3. **Technical Issue**
   - Subject: "The app keeps crashing on my phone"
   - Body: App crash problem

4. **Complaint**
   - Subject: "Your service is terrible! I want a refund"
   - Body: Unhappy customer feedback

Click any template to auto-fill the form!

#### Sending an Email

1. Fill in the form fields
2. (Optional) Click a quick template to pre-fill
3. Click **"Send Test Email"** button
4. Wait for processing (shows spinner)
5. View the result below the form

#### Processing Result

Shows detailed information about the email processing:

- **Status**: `completed` or `pending_review`
- **Email ID**: Unique identifier for the email
- **Category**: Classified email type
- **Priority**: high, normal, or low
- **Sent**: Whether a response was sent
- **Human Review**: Whether escalated to human agent

### Tab 2: Inbox

View all processed emails in a structured list.

#### Statistics Dashboard

Four key metrics:

1. **Total Emails** - Total number of emails processed
2. **Sent** - Emails where response was automatically sent
3. **Pending Review** - Emails awaiting human review
4. **Errors** - Emails with processing errors

Updates automatically every 10 seconds.

#### Filtering Options

**Filter by Status:**
- All (default)
- Completed (response sent)
- Pending Review (awaiting human)

**Filter by Category:**
- All (default)
- Technical Support
- Billing
- General Inquiry
- Complaint
- Feature Request

Apply filters by selecting from dropdowns.

#### Email List

Each email shows:

- **From**: Sender's email address
- **Subject**: Email subject line
- **Timestamp**: Date and time received
- **Category Badge**: Email classification
- **Status Badge**: Processing status (Sent/Pending)

Click any email to view full details!

#### Email Detail Modal

Opens when you click an email. Shows:

**Email Information:**
- From address
- Subject line
- Received date/time
- Full email body

**Agent Processing:**
- Status (Completed/Pending Review)
- Category assigned
- Priority level
- Whether response was sent
- Whether human review is required
- Whether follow-up was scheduled
- Any errors encountered

**Additional Details:**
- Complete agent response data in JSON format
- Knowledge base search results
- Classification confidence
- Processing metadata

## Common Workflows

### Workflow 1: Test a Single Email

1. Go to **Test Email** tab
2. Click a quick template (e.g., "Login Issue")
3. Click **Send Test Email**
4. View the result
5. Go to **Inbox** to see it listed

### Workflow 2: Test Multiple Scenarios

1. Send "Login Issue" email
2. Send "Billing Issue" email
3. Send "Complaint" email
4. Go to **Inbox**
5. View statistics - see which were sent vs. escalated

### Workflow 3: Monitor Processing

1. Go to **Inbox** tab
2. Review statistics
3. Filter by "Pending Review" to see escalated emails
4. Click on emails to view agent's reasoning

### Workflow 4: Analyze by Category

1. Go to **Inbox** tab
2. Filter by Category: "Technical Support"
3. Review all technical emails
4. Check which were auto-responded vs. escalated

## Understanding Email Status

### Status: Completed

✅ Email was processed successfully
✅ Agent provided an automatic response
✅ Customer will receive the response

### Status: Pending Review

⚠️ Email is awaiting human agent review
⚠️ Reasons might include:
- High-priority issue
- Complaint or negative feedback
- No relevant documentation found
- Low classification confidence
- Requires human expertise

## Understanding Email Categories

| Category | Description | Typical Response |
|----------|-------------|-----------------|
| **Technical Support** | Software issues, bugs, crashes | Auto-response with KB solution |
| **Billing** | Payment, refund, subscription issues | Escalated to billing team |
| **General Inquiry** | Product info, account questions | Auto-response from KB |
| **Complaint** | Negative feedback, service issues | Escalated to management |
| **Feature Request** | Enhancement suggestions | Auto-response with thank you |
| **Other** | Unknown category | Escalated for review |

## Tips and Tricks

### View Processing Details

Click on any email in the inbox to see:
- Full email content
- Knowledge base search results
- Classification reasoning
- Complete agent output

### Test Edge Cases

Use custom emails to test:
- Very short messages
- Very long messages
- Spam-like content
- Multiple languages (if supported)
- Special characters

### Monitor Knowledge Base

View which knowledge base documents are being used:
1. Click on an email
2. Look at "Additional Details" section
3. Search results show knowledge base relevance

### Track Agent Performance

Use statistics to track:
- Total emails processed
- Automation rate (Sent vs. Pending Review)
- Error rate
- Distribution by category

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| Tab | Focus next form field |
| Enter | Submit form (when focused on submit button) |
| Escape | Close email detail modal |

## Responsive Design

The UI adapts to different screen sizes:

- **Desktop (1024px+)** - Full layout with all details
- **Tablet (768-1023px)** - Optimized grid layout
- **Mobile (< 768px)** - Stacked layout, touch-friendly

## Dark Mode

The UI uses a light theme with good contrast. Future updates may include dark mode support.

## Troubleshooting

### Email Won't Send

**Problem**: "Send Test Email" button shows error

**Solutions**:
- Check email address format (must be valid)
- Ensure subject and body are not empty
- Check browser console for error messages
- Verify API is running

### Inbox Won't Load

**Problem**: Empty inbox or "No emails yet" message

**Solutions**:
- Send a test email first
- Refresh the page (Ctrl+R)
- Check if API is running
- Check browser network tab for errors

### Modal Won't Close

**Problem**: Email detail modal stays open

**Solutions**:
- Click the X button in top right
- Press Escape key
- Click outside the modal
- Refresh the page

### Statistics Not Updating

**Problem**: Stats show 0 or wrong numbers

**Solutions**:
- Refresh the page
- Wait 10 seconds (auto-refresh interval)
- Click "Refresh" button in Inbox tab
- Check browser console

## API Integration

The UI connects to these API endpoints:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/emails/process` | POST | Send email for processing |
| `/inbox` | GET | Get all emails |
| `/inbox/{email_id}` | GET | Get email details |
| `/inbox/stats` | GET | Get statistics |
| `/inbox/filter/status/{status}` | GET | Filter by status |
| `/inbox/filter/category/{category}` | GET | Filter by category |

All requests are made from the browser via JavaScript.

## Data Storage

Emails are stored **in memory** during the session:

- Data persists while the server is running
- Data is lost when server restarts
- Perfect for testing and development
- For production, implement database storage

## Customization

### Add New Quick Templates

Edit `frontend/app.js`:

```javascript
const emailTemplates = {
    // ... existing templates
    custom: {
        subject: "Your Subject",
        body: "Your email body"
    }
};
```

Add button to HTML:
```html
<button type="button" class="template-btn" data-template="custom">
    Custom Template
</button>
```

### Change Colors

Edit `frontend/styles.css`:

```css
:root {
    --primary-color: #your-color;
    --secondary-color: #your-color;
    /* ... etc */
}
```

### Add New Fields

Edit `frontend/index.html` to add form fields.

## Performance

- Fast loading (< 1 second)
- Responsive interactions
- Auto-refreshes every 10 seconds
- Smooth animations
- Works offline (once loaded)

## Browser Compatibility

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+
- Mobile Safari (iOS 14+)
- Chrome Mobile (Android 90+)

## Security Notes

The UI is designed for **internal testing only**:

- No authentication implemented
- All data is client-side
- API has CORS enabled for testing
- For production, add authentication

## Future Enhancements

Potential improvements:

- [ ] Dark mode
- [ ] Email search
- [ ] Bulk actions
- [ ] Export emails
- [ ] Database persistence
- [ ] Authentication
- [ ] User roles
- [ ] Email analytics
- [ ] Rate limiting dashboard
- [ ] Real-time notifications

## Getting Help

1. Check browser console (F12) for errors
2. Review API logs
3. Check README.md for general setup
4. Review WORKFLOW.md for workflow details

---

**The UI is ready to use! Start the server and navigate to http://localhost:8000** 🚀