// Email templates for quick testing
const emailTemplates = {
    login: {
        subject: "I cannot login to my account",
        body: "I've tried resetting my password but I'm not receiving the email. Can someone help me?"
    },
    billing: {
        subject: "I was charged twice for my subscription",
        body: "I noticed two charges on my account for the same month. Can you please investigate and refund the duplicate charge?"
    },
    technical: {
        subject: "The app keeps crashing on my phone",
        body: "The mobile app crashes every time I try to export my data. This is very frustrating and affects my workflow."
    },
    complaint: {
        subject: "Your service is terrible! I want a refund",
        body: "I'm very dissatisfied with this service. The support is unresponsive and the features don't work as advertised. I demand a refund immediately!"
    }
};

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    setupEventListeners();
    refreshInbox();
});

// Setup event listeners
function setupEventListeners() {
    // Tab navigation
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            switchTab(this.dataset.tab);
        });
    });

    // Email form
    document.getElementById('email-form').addEventListener('submit', handleEmailSubmit);

    // Template buttons
    document.querySelectorAll('.template-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const template = emailTemplates[this.dataset.template];
            document.getElementById('subject').value = template.subject;
            document.getElementById('body').value = template.body;
        });
    });

    // Filters
    document.getElementById('filter-status').addEventListener('change', applyFilters);
    document.getElementById('filter-category').addEventListener('change', applyFilters);
}

// Switch between tabs
function switchTab(tabName) {
    // Update active tab
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    document.getElementById(tabName).classList.add('active');
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');

    // Refresh data if needed
    if (tabName === 'inbox-tab') {
        refreshInbox();
    }
}

// Handle email form submission
async function handleEmailSubmit(e) {
    e.preventDefault();

    const sender = document.getElementById('sender').value;
    const subject = document.getElementById('subject').value;
    const body = document.getElementById('body').value;

    const submitBtn = document.getElementById('submit-btn');
    const btnText = submitBtn.querySelector('.btn-text');
    const spinner = submitBtn.querySelector('.spinner');

    submitBtn.disabled = true;
    btnText.style.display = 'none';
    spinner.style.display = 'block';

    try {
        const response = await fetch('/api/v1/emails/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                sender,
                subject,
                body
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        displayResult(result);

        // Refresh inbox
        setTimeout(refreshInbox, 1000);

    } catch (error) {
        console.error('Error:', error);
        alert('Error processing email: ' + error.message);
    } finally {
        submitBtn.disabled = false;
        btnText.style.display = 'inline';
        spinner.style.display = 'none';
    }
}

// Display processing result
function displayResult(result) {
    const container = document.getElementById('result-container');
    const content = document.getElementById('result-content');

    let html = '';

    // Status section
    html += `
        <div class="result-section">
            <h4>Status</h4>
            <div class="status-badge ${result.status}">
                ${result.status.replace('_', ' ').toUpperCase()}
            </div>
    `;

    // Email ID
    html += `
        <div class="result-item">
            <div class="result-label">Email ID</div>
            <div class="result-value">${result.email_id}</div>
        </div>
    `;

    html += '</div>';

    // Classification section
    if (result.metadata) {
        html += `
            <div class="result-section">
                <h4>Classification</h4>
                <div class="result-item">
                    <div class="result-label">Category</div>
                    <div class="result-value">${result.metadata.category || 'N/A'}</div>
                </div>
                <div class="result-item">
                    <div class="result-label">Priority</div>
                    <div class="result-value">${result.metadata.priority || 'N/A'}</div>
                </div>
                <div class="result-item">
                    <div class="result-label">Sent</div>
                    <div class="result-value">${result.metadata.sent ? '✅ Yes' : '❌ No'}</div>
                </div>
                <div class="result-item">
                    <div class="result-label">Human Review</div>
                    <div class="result-value">${result.metadata.requires_human_review ? '⚠️ Required' : '✅ Not Required'}</div>
                </div>
            </div>
        `;
    }

    // Error section
    if (result.error) {
        html += `
            <div class="result-section">
                <h4>Error</h4>
                <div class="status-badge error">${result.error}</div>
            </div>
        `;
    }

    content.innerHTML = html;
    container.style.display = 'block';
    container.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

// Close result container
function closeResult() {
    document.getElementById('result-container').style.display = 'none';
}

// Refresh inbox
async function refreshInbox() {
    try {
        const response = await fetch('/inbox');
        const data = await response.json();

        displayInboxList(data.emails);
        updateStats();

    } catch (error) {
        console.error('Error fetching inbox:', error);
    }
}

// Display inbox list
function displayInboxList(emails) {
    const container = document.getElementById('inbox-list');

    if (emails.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <p>No emails yet. Send a test email to get started!</p>
            </div>
        `;
        return;
    }

    let html = '';
    emails.forEach(email => {
        const statusClass = email.status === 'completed' ? 'sent' : 'pending';
        const categoryBadge = email.category ? `<span class="email-badge ${email.category}">${email.category.replace('_', ' ')}</span>` : '';

        html += `
            <div class="email-item" onclick="viewEmailDetail('${email.id}')">
                <div class="email-item-content">
                    <div class="email-item-header">
                        <div>
                            <div class="email-from">${email.sender}</div>
                            <div class="email-subject">${email.subject}</div>
                            <div class="email-timestamp">${new Date(email.timestamp).toLocaleString()}</div>
                        </div>
                    </div>
                    <div class="email-meta">
                        ${categoryBadge}
                        <span class="email-status ${statusClass}">${email.status}</span>
                    </div>
                </div>
            </div>
        `;
    });

    container.innerHTML = html;
}

// Update inbox statistics
async function updateStats() {
    try {
        const response = await fetch('/inbox/stats');
        const stats = response.json();

        stats.then(data => {
            document.getElementById('total-count').textContent = data.total_emails;
            document.getElementById('sent-count').textContent = data.sent_emails;
            document.getElementById('review-count').textContent = data.pending_review;
            document.getElementById('error-count').textContent = data.with_errors;
        });

    } catch (error) {
        console.error('Error fetching statistics:', error);
    }
}

// View email detail
async function viewEmailDetail(emailId) {
    try {
        const response = await fetch(`/inbox/${emailId}`);
        const email = await response.json();

        displayEmailDetail(email);

    } catch (error) {
        console.error('Error fetching email detail:', error);
        alert('Error loading email details');
    }
}

// Display email detail in modal
function displayEmailDetail(email) {
    const modal = document.getElementById('email-detail-modal');
    const subject = document.getElementById('detail-subject');
    const body = document.getElementById('detail-body');

    subject.textContent = email.subject;

    let html = `
        <div class="detail-section">
            <div class="detail-section-title">Email Information</div>
            <div class="detail-field">
                <div class="detail-label">From</div>
                <div class="detail-value">${email.sender}</div>
            </div>
            <div class="detail-field">
                <div class="detail-label">Subject</div>
                <div class="detail-value">${email.subject}</div>
            </div>
            <div class="detail-field">
                <div class="detail-label">Date</div>
                <div class="detail-value">${new Date(email.timestamp).toLocaleString()}</div>
            </div>
            <div class="detail-field">
                <div class="detail-label">Body</div>
                <div class="detail-value">${escapeHtml(email.body)}</div>
            </div>
        </div>

        <div class="detail-section">
            <div class="detail-section-title">Agent Processing</div>
            <div class="detail-field">
                <div class="detail-label">Status</div>
                <div class="detail-value">
                    <span class="status-badge ${email.status}">${email.status.replace('_', ' ').toUpperCase()}</span>
                </div>
            </div>
            <div class="detail-field">
                <div class="detail-label">Category</div>
                <div class="detail-value">${email.category || 'N/A'}</div>
            </div>
            <div class="detail-field">
                <div class="detail-label">Priority</div>
                <div class="detail-value">${email.priority || 'N/A'}</div>
            </div>
            <div class="detail-field">
                <div class="detail-label">Email Sent</div>
                <div class="detail-value">${email.sent ? '✅ Yes' : '❌ No'}</div>
            </div>
            <div class="detail-field">
                <div class="detail-label">Human Review Required</div>
                <div class="detail-value">${email.requires_human_review ? '⚠️ Yes' : '✅ No'}</div>
            </div>
            <div class="detail-field">
                <div class="detail-label">Follow-up Scheduled</div>
                <div class="detail-value">${email.follow_up_scheduled ? '✅ Yes' : '❌ No'}</div>
            </div>
    `;

    if (email.error) {
        html += `
            <div class="detail-field">
                <div class="detail-label">Error</div>
                <div class="detail-value">${escapeHtml(email.error)}</div>
            </div>
        `;
    }

    html += '</div>';

    // Add more details from full result if available
    if (email.full_result) {
        html += `
            <div class="detail-section">
                <div class="detail-section-title">Additional Details</div>
                <pre style="background: #f3f4f6; padding: 12px; border-radius: 4px; overflow-x: auto; font-size: 12px;">
${JSON.stringify(email.full_result, null, 2)}
                </pre>
            </div>
        `;
    }

    body.innerHTML = html;
    modal.style.display = 'flex';
}

// Close modal
function closeModal() {
    document.getElementById('email-detail-modal').style.display = 'none';
}

// Apply filters
async function applyFilters() {
    const status = document.getElementById('filter-status').value;
    const category = document.getElementById('filter-category').value;

    try {
        let url = '/inbox';

        if (status) {
            url = `/inbox/filter/status/${status}`;
        } else if (category) {
            url = `/inbox/filter/category/${category}`;
        }

        const response = await fetch(url);
        const data = await response.json();

        displayInboxList(data.emails);

    } catch (error) {
        console.error('Error applying filters:', error);
    }
}

// Utility function to escape HTML
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

// Auto-refresh inbox every 10 seconds
setInterval(function() {
    const activeTab = document.querySelector('.tab-content.active').id;
    if (activeTab === 'inbox-tab') {
        refreshInbox();
    }
}, 10000);