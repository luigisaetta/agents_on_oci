"""
Define the structure of the document to be created
"""

STRUCTURE = """
## List of sections and their description: 

### 1. Table of Contents
**Description:** This section provides a well-formatted table of contents, where all the other sections are listed.
**Special Instructions:** Don't put the number of the pages.

### 2. Overview
**Description:** This section provides a high-level summary of the Proof of Concept (PoC) objectives, key stakeholders, and the intended business impact. It should clearly state the purpose and scope of the PoC, including any background on why the initiative is being undertaken.
**Special Instructions:** put the name of the customer in bold

### 3. Scope and Approach
**Description:** Defines the boundaries of the PoC, including the technologies, platforms, and specific solutions to be tested. This section should detail:
   - The key components and services involved.
   - The specific technical configurations required.
   - The method and approach for testing and evaluating the PoC.
**Special Instructions:** put the name of the customer in bold

### 4. Timelines
**Description:** Presents the detailed timeline of the PoC, breaking it down into key phases with estimated durations. Each phase should have:
   - Specific tasks to be completed.
   - Assigned owners or responsible teams.
   - Milestones to measure progress.

### 5. Proof of Concept Architecture
**Description:** This section provides a detailed technical architecture diagram and description of the system setup. It should include:
   - Hardware and software components.
   - Cloud infrastructure setup (e.g., OCI, Kubernetes, Networking, Security).
   - Data flow and integration with existing systems.

### 6. Success Criteria
**Description:** Defines the key performance indicators (KPIs) and measurable outcomes that will determine the success of the PoC. Examples include:
   - System performance improvements.
   - Ease of deployment and scalability.
   - Improved business outcomes such as efficiency and cost savings.

### 7. Use Cases
**Description:** Lists the specific business and technical use cases that the PoC aims to validate. Each use case should include:
   - The business problem it addresses.
   - Expected outcome and benefits.
   - Required resources and dependencies.

### 8. Deliverables
**Description:** Specifies the final outputs of the PoC, including:
   - A working production-level environment.
   - A comprehensive PoC report with results and recommendations.
   - Documentation on implementation, challenges, and next steps.

### 9. Proof of Concept Requirements
**Description:** Outlines the infrastructure, software, and personnel required for the PoC execution. This includes:
   - Cloud resources (IaaS, PaaS, SaaS solutions).
   - Necessary configurations and integrations.
   - Security and compliance considerations.

### 10. Risk Assessment
**Description:** Identifies potential risks during the PoC execution and provides mitigation strategies. Covers:
   - Technical risks (e.g., infrastructure failures, software compatibility issues).
   - Operational risks (e.g., timeline delays, resource limitations).
   - Business risks (e.g., unmet ROI expectations, regulatory constraints).

### 11. Multi-Cloud Considerations
**Description:** If applicable, discusses PoC compatibility with multi-cloud environments, including:
   - Performance and integration across different cloud providers.
   - Security measures for data sharing and interoperability.

### 12. Data Migration Strategy
**Description:** Provides details on how data will be migrated from existing environments. Covers:
   - Tools and processes for secure data transfer.
   - Expected challenges and mitigation plans.

### 13. AI/ML Performance Metrics
**Description:** For AI-based PoCs, outlines how model performance will be evaluated, including:
   - Accuracy, inference time, and resource consumption.
   - Comparisons against existing solutions.

### 14. Security & Compliance
**Description:** Details security measures in place to ensure data protection and regulatory compliance, covering:
   - Identity and access management (IAM).
   - Encryption, logging, and auditing.
   - Industry-specific compliance requirements.

### 15. User Acceptance Testing (UAT)
**Description:** Describes the process for validating PoC results with users, including:
   - Criteria for user acceptance before full-scale deployment.
   - Feedback collection methods.

### 16. Post-PoC Recommendations
**Description:** Suggests next steps based on PoC results, including:
   - Potential full-scale implementation roadmap.
   - Additional optimizations or iterations needed before deployment.

## **17. Contacts**
**Description**:** The list of contacts, with their role and emails
**Special Instructions:** organize the contacts' information in a well-formatted table
| Name  | Role | Email |  
|-------|------|-------|  
| {Contact Name 1} | {Role} | {Email} |  
| {Contact Name 2} | {Role} | {Email} |  
| {Contact Name 3} | {Role} | {Email} | 

## **18. Acronyms**
**Description**:** The list of all acronyms contained in the text, with their explanation.
**Special Instructions:** This is a mandatory section.

"""
