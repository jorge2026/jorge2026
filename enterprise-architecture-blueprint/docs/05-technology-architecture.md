# 05 — Technology Architecture

## 1. Technology domains

| Domain | Target capability | Design considerations |
|---|---|---|
| Cloud and hosting | Hybrid and multicloud hosting where justified | Workload placement, portability, resilience, exit strategy |
| Network | Segmented connectivity and controlled ingress/egress | Zero-trust principles, DNS, private connectivity |
| Compute | Containers, serverless, and managed compute | Operational model, scaling, workload fit |
| Platform engineering | Standardized landing zones and reusable services | Golden paths, policy as code, developer experience |
| Integration | API management and event messaging | Security, contracts, delivery guarantees |
| Data platform | Governed storage and processing | Data residency, lifecycle, access, cost |
| AI platform | Approved model access and evaluation | Safety, privacy, model risk, observability |
| Security | Identity, key management, posture and detection | Least privilege, threat modeling, audit |
| Operations | Monitoring, incident, backup and recovery | SLOs, RTO/RPO, support ownership |

## 2. Reference deployment patterns

- Use managed cloud services when they satisfy business, security, resilience, and financial requirements.
- Use Kubernetes for workloads that benefit from container orchestration and its operational model; do not make every workload a Kubernetes workload.
- Use serverless for event-driven or variable workloads where execution constraints and economics fit.
- Use Infrastructure as Code and policy as code to standardize repeatable environments.
- Separate development, test, and production environments with appropriate identity, network, and data boundaries.
- Define recovery architecture according to business impact and approved RTO/RPO.

## 3. Cross-cutting non-functional requirements

| Attribute | Architecture question |
|---|---|
| Availability | What service level is required and measured? |
| Performance | What are workload latency and throughput needs? |
| Scalability | Which dimensions scale and what are the limits? |
| Security | What are the trust boundaries and threat scenarios? |
| Privacy | What personal or sensitive data is processed? |
| Resilience | How does the service behave under dependency failure? |
| Operability | Who monitors, supports, and changes the service? |
| Cost | What is the cost driver and who owns optimization? |
| Portability | What is the real business value of portability? |

## 4. FinOps architecture

- Establish account, subscription, project, and tag/label standards.
- Allocate costs to business services, products, and owners where possible.
- Track unit economics such as cost per transaction or cost per customer served when data supports it.
- Set budgets, anomaly alerts, and review cadences.
- Evaluate architecture trade-offs using total cost of ownership, not compute price alone.

## 5. Technology standards lifecycle

Each standard should have an owner, rationale, applicability, exception process, review date, and lifecycle state (emerging, strategic, tolerated, or retiring).
