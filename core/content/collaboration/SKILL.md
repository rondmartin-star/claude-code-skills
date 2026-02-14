---
name: collaboration
description: >
  Enable team collaboration on corpus content through comments, change proposals, review workflows,
  and approval processes. Integrates with CorpusHub for centralized collaboration features.
---

# Collaboration

**Purpose:** Team collaboration, comments, proposals, and approval workflows
**Size:** ~14 KB
**Type:** Core Content Management (Universal)
**Status:** Production

---

## ⚡ LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "Add comment to this section"
- "Propose changes to..."
- "Submit for review"
- "Approve this document"
- "Request feedback on..."
- "Create change proposal"

**Context Indicators:**
- Team review needed
- Comments/feedback required
- Approval workflow
- Change proposal
- Collaborative editing

## ❌ DO NOT LOAD WHEN

- Solo content editing (use review-edit-author)
- Version control (use version-control)
- Document management (use document-management)

---

## Core Features

### Comments

#### Add Comment

```javascript
async function addComment(target, commentText, options = {}) {
  const {
    author = 'Claude Code',
    type = 'general', // 'general', 'suggestion', 'issue', 'question'
    resolved = false,
    lineNumber = null,
    section = null
  } = options;

  const comment = {
    id: generateUniqueId(),
    target,
    text: commentText,
    author,
    type,
    resolved,
    lineNumber,
    section,
    timestamp: new Date(),
    replies: []
  };

  // Save to comments file
  await saveComment(target, comment);

  // Sync to CorpusHub if applicable
  if (await isCorpusHubEnabled()) {
    await syncCommentToHub(comment);
  }

  console.log(`✓ Comment added by ${author}`);
  return comment;
}
```

#### Reply to Comment

```javascript
async function replyToComment(commentId, replyText, options = {}) {
  const {
    author = 'Claude Code'
  } = options;

  const comment = await findComment(commentId);

  if (!comment) {
    throw new Error(`Comment not found: ${commentId}`);
  }

  const reply = {
    id: generateUniqueId(),
    author,
    text: replyText,
    timestamp: new Date()
  };

  comment.replies.push(reply);
  await updateComment(comment);

  console.log(`✓ Reply added by ${author}`);
  return reply;
}
```

#### Resolve Comment

```javascript
async function resolveComment(commentId, resolvedBy) {
  const comment = await findComment(commentId);

  if (!comment) {
    throw new Error(`Comment not found: ${commentId}`);
  }

  comment.resolved = true;
  comment.resolvedBy = resolvedBy;
  comment.resolvedAt = new Date();

  await updateComment(comment);

  console.log(`✓ Comment resolved by ${resolvedBy}`);
  return comment;
}
```

#### List Comments

```javascript
async function listComments(target, options = {}) {
  const {
    includeResolved = false,
    type = null,
    author = null
  } = options;

  const allComments = await loadComments(target);

  let filtered = allComments;

  // Filter by resolution status
  if (!includeResolved) {
    filtered = filtered.filter(c => !c.resolved);
  }

  // Filter by type
  if (type) {
    filtered = filtered.filter(c => c.type === type);
  }

  // Filter by author
  if (author) {
    filtered = filtered.filter(c => c.author === author);
  }

  return filtered;
}
```

---

### Change Proposals

#### Create Proposal

```javascript
async function createChangeProposal(target, changes, options = {}) {
  const {
    title,
    description,
    author = 'Claude Code',
    reviewers = [],
    priority = 'normal' // 'low', 'normal', 'high', 'critical'
  } = options;

  const proposal = {
    id: generateUniqueId(),
    target,
    title,
    description,
    author,
    changes: {
      before: await readFile(target),
      after: changes
    },
    reviewers,
    priority,
    status: 'pending', // 'pending', 'approved', 'rejected', 'revised'
    createdAt: new Date(),
    reviews: [],
    approvals: []
  };

  await saveProposal(proposal);

  // Notify reviewers
  if (reviewers.length > 0) {
    await notifyReviewers(proposal, reviewers);
  }

  console.log(`✓ Change proposal created: ${proposal.id}`);
  console.log(`  Title: ${title}`);
  console.log(`  Reviewers: ${reviewers.join(', ')}`);

  return proposal;
}
```

#### Review Proposal

```javascript
async function reviewProposal(proposalId, review, options = {}) {
  const {
    reviewer = 'Claude Code',
    decision = 'comment', // 'approve', 'reject', 'request-changes', 'comment'
    comments = []
  } = options;

  const proposal = await loadProposal(proposalId);

  if (!proposal) {
    throw new Error(`Proposal not found: ${proposalId}`);
  }

  const reviewEntry = {
    id: generateUniqueId(),
    reviewer,
    decision,
    review,
    comments,
    timestamp: new Date()
  };

  proposal.reviews.push(reviewEntry);

  // Update proposal status based on decision
  if (decision === 'approve') {
    proposal.approvals.push(reviewer);

    // Check if all required approvals received
    if (hasAllApprovals(proposal)) {
      proposal.status = 'approved';
      console.log('✓ Proposal fully approved');
    }
  } else if (decision === 'reject') {
    proposal.status = 'rejected';
  } else if (decision === 'request-changes') {
    proposal.status = 'revised';
  }

  await updateProposal(proposal);

  console.log(`✓ Review submitted by ${reviewer}: ${decision}`);
  return reviewEntry;
}
```

#### Apply Proposal

```javascript
async function applyProposal(proposalId, options = {}) {
  const {
    confirmApply = true,
    createBackup = true
  } = options;

  const proposal = await loadProposal(proposalId);

  if (!proposal) {
    throw new Error(`Proposal not found: ${proposalId}`);
  }

  // Check if approved
  if (proposal.status !== 'approved') {
    console.warn(`⚠️  Proposal status: ${proposal.status}`);
    console.log('Only approved proposals should be applied.');
    console.log('');
    console.log('Force apply anyway? [y/N]');

    const proceed = await promptUser();
    if (!proceed) {
      return { applied: false };
    }
  }

  // Confirmation
  if (confirmApply) {
    console.log('Apply approved changes to:');
    console.log(`  ${proposal.target}`);
    console.log('');
    console.log('Continue? [Y/n]');

    const proceed = await promptUser();
    if (!proceed) {
      return { applied: false };
    }
  }

  // Backup current version
  if (createBackup) {
    await createBackupCopy(proposal.target);
  }

  // Apply changes
  await writeFile(proposal.target, proposal.changes.after);

  // Update proposal
  proposal.status = 'applied';
  proposal.appliedAt = new Date();
  await updateProposal(proposal);

  console.log('✓ Proposal applied successfully');
  return { applied: true, proposal };
}
```

---

### Review Workflows

#### Submit for Review

```javascript
async function submitForReview(target, options = {}) {
  const {
    reviewers = [],
    reviewType = 'general', // 'general', 'technical', 'editorial', 'security'
    deadline = null,
    checklist = []
  } = options;

  const review = {
    id: generateUniqueId(),
    target,
    reviewType,
    reviewers,
    deadline,
    checklist,
    status: 'in-review',
    submittedAt: new Date(),
    submittedBy: 'Claude Code',
    feedback: [],
    completed: false
  };

  await saveReview(review);

  // Notify reviewers
  await notifyReviewers(review, reviewers);

  console.log('✓ Submitted for review');
  console.log(`  Reviewers: ${reviewers.join(', ')}`);
  if (deadline) {
    console.log(`  Deadline: ${deadline.toLocaleDateString()}`);
  }

  return review;
}
```

#### Complete Review

```javascript
async function completeReview(reviewId, feedback, options = {}) {
  const {
    reviewer = 'Claude Code',
    approved = true
  } = options;

  const review = await loadReview(reviewId);

  if (!review) {
    throw new Error(`Review not found: ${reviewId}`);
  }

  const feedbackEntry = {
    reviewer,
    approved,
    feedback,
    timestamp: new Date()
  };

  review.feedback.push(feedbackEntry);

  // Check if all reviewers have completed
  if (review.feedback.length >= review.reviewers.length) {
    review.completed = true;
    review.completedAt = new Date();

    // Determine overall status
    const allApproved = review.feedback.every(f => f.approved);
    review.status = allApproved ? 'approved' : 'changes-requested';
  }

  await updateReview(review);

  console.log(`✓ Review completed by ${reviewer}`);
  console.log(`  Approved: ${approved ? 'Yes' : 'No'}`);

  return feedbackEntry;
}
```

---

### Approval Workflows

#### Request Approval

```javascript
async function requestApproval(target, options = {}) {
  const {
    approvers = [],
    requiredApprovals = approvers.length, // All by default
    description = '',
    urgency = 'normal'
  } = options;

  const approval = {
    id: generateUniqueId(),
    target,
    description,
    approvers,
    requiredApprovals,
    urgency,
    status: 'pending',
    requestedAt: new Date(),
    requestedBy: 'Claude Code',
    approvals: [],
    rejections: []
  };

  await saveApproval(approval);

  // Notify approvers
  await notifyApprovers(approval, approvers);

  console.log('✓ Approval requested');
  console.log(`  Approvers: ${approvers.join(', ')}`);
  console.log(`  Required: ${requiredApprovals}/${approvers.length}`);

  return approval;
}
```

#### Approve/Reject

```javascript
async function respondToApproval(approvalId, decision, options = {}) {
  const {
    approver = 'Claude Code',
    comments = ''
  } = options;

  const approval = await loadApproval(approvalId);

  if (!approval) {
    throw new Error(`Approval not found: ${approvalId}`);
  }

  const response = {
    approver,
    decision, // 'approve' or 'reject'
    comments,
    timestamp: new Date()
  };

  if (decision === 'approve') {
    approval.approvals.push(response);
  } else {
    approval.rejections.push(response);
  }

  // Update status
  if (approval.rejections.length > 0) {
    approval.status = 'rejected';
  } else if (approval.approvals.length >= approval.requiredApprovals) {
    approval.status = 'approved';
  }

  await updateApproval(approval);

  console.log(`✓ ${decision === 'approve' ? 'Approved' : 'Rejected'} by ${approver}`);
  console.log(`  Status: ${approval.status}`);

  return response;
}
```

---

---

## CorpusHub Integration

### Sync Comments to CorpusHub

```javascript
async function syncCommentToHub(comment) {
  const hubStatus = await checkCorpusHubStatus();

  if (!hubStatus.running) {
    console.warn('⚠️  CorpusHub not running - comment saved locally only');
    return { synced: false };
  }

  const response = await fetch('http://localhost:3000/api/comments/create', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      bitId: await getBitIdForFile(comment.target),
      text: comment.text,
      author: comment.author,
      type: comment.type,
      lineNumber: comment.lineNumber,
      section: comment.section
    })
  });

  if (response.ok) {
    const hubComment = await response.json();
    comment.hubId = hubComment.id;
    await updateComment(comment);
    return { synced: true, hubId: hubComment.id };
  } else {
    return { synced: false };
  }
}
```

---

## Display Functions

### Show Comments for Document

```javascript
async function showComments(target, options = {}) {
  const comments = await listComments(target, options);

  if (comments.length === 0) {
    console.log('No comments found.');
    return;
  }

  console.log(`Comments for ${path.basename(target)}:`);
  console.log('');

  for (const comment of comments) {
    const icon = comment.type === 'issue' ? '🔴'
                : comment.type === 'suggestion' ? '💡'
                : comment.type === 'question' ? '❓'
                : '💬';

    console.log(`${icon} ${comment.author} - ${comment.timestamp.toLocaleString()}`);
    if (comment.lineNumber) {
      console.log(`   Line ${comment.lineNumber}`);
    }
    if (comment.section) {
      console.log(`   Section: ${comment.section}`);
    }
    console.log(`   ${comment.text}`);

    if (comment.replies.length > 0) {
      for (const reply of comment.replies) {
        console.log(`     ↳ ${reply.author}: ${reply.text}`);
      }
    }

    if (comment.resolved) {
      console.log(`   ✓ Resolved by ${comment.resolvedBy}`);
    }

    console.log('');
  }

  console.log(`Total: ${comments.length} comments`);
}
```

---

## Configuration

```json
{
  "collaboration": {
    "comments": {
      "autoResolveOnApply": false,
      "syncToHub": true,
      "notifyOnReply": true
    },
    "proposals": {
      "requireApproval": true,
      "minApprovals": 1,
      "allowSelfApprove": false
    },
    "reviews": {
      "defaultReviewers": [],
      "requireAllApprovals": false,
      "sendReminders": true
    },
    "notifications": {
      "method": "email", // 'email', 'slack', 'hub'
      "enabled": true
    }
  }
}
```

---

## Usage Examples

### Example 1: Comment Workflow

```
# Add comment
await addComment('docs/api.md', 'This section needs more examples', {
  type: 'suggestion',
  section: 'Authentication'
});

# Reply to comment
await replyToComment(commentId, 'Good point, I'll add them');

# Resolve comment
await resolveComment(commentId, 'Claude Code');
```

### Example 2: Change Proposal

```
# Create proposal
const proposal = await createChangeProposal('docs/api.md', newContent, {
  title: 'Update authentication examples',
  reviewers: ['alice', 'bob']
});

# Review
await reviewProposal(proposal.id, 'Looks good!', {
  decision: 'approve',
  reviewer: 'alice'
});

# Apply when approved
await applyProposal(proposal.id);
```

### Example 3: Approval Workflow

```
# Request approval
await requestApproval('docs/api.md', {
  approvers: ['tech-lead', 'product-manager'],
  requiredApprovals: 2
});

# Approve
await respondToApproval(approvalId, 'approve', {
  approver: 'tech-lead'
});
```

---

## Quick Reference

**Add comment:**
```javascript
await addComment(filePath, 'Your comment');
```

**Create proposal:**
```javascript
await createChangeProposal(filePath, newContent, {
  title: 'Description',
  reviewers: ['user1', 'user2']
});
```

**Request approval:**
```javascript
await requestApproval(filePath, {
  approvers: ['approver1'],
  requiredApprovals: 1
});
```

---

*End of Collaboration*
*Part of v4.0.0 Universal Skills Ecosystem*
*Integrates with: CorpusHub, review-edit-author*
