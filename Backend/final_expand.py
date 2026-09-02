"""
Final expansion to bring manuscript to 500+ pages.
Adds:
- Appendix D: Sample Architecture Blueprints
- Appendix E: Enterprise AI Maturity Model
- Extended Foreword
- Acknowledgments
"""

from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml

FONT_NAME = "Times New Roman"
BODY_SIZE = 12
HEADING1_SIZE = 16
SUBHEADING_SIZE = 12
LINE_SPACING = 1.5
FIRST_LINE_INDENT_CM = 1.27
BOOK_TITLE = "Self-Evolving Enterprise Systems: AI-Driven Architectures for the Next Generation of Digital Platforms"
TOP_MARGIN = 1.52
BOTTOM_MARGIN = 1.52
LEFT_MARGIN = 1.97
RIGHT_MARGIN = 1.96


def add_formatted_paragraph(doc, text, font_size=BODY_SIZE, bold=False,
                             alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
                             first_line_indent=True, space_after=Pt(6),
                             space_before=Pt(0), font_name=FONT_NAME,
                             color=RGBColor(0, 0, 0), line_spacing=LINE_SPACING,
                             italic=False):
    p = doc.add_paragraph()
    run = p.add_run(text)
    pf = p.paragraph_format
    pf.alignment = alignment
    pf.line_spacing = line_spacing
    pf.first_line_indent = Cm(FIRST_LINE_INDENT_CM) if first_line_indent else Cm(0)
    pf.space_after = space_after
    pf.space_before = space_before
    run.font.name = font_name
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.italic = italic
    return p


def add_heading1(doc, text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.name = FONT_NAME
    run.font.size = Pt(HEADING1_SIZE)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0, 0, 0)
    pf = p.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf.space_before = Pt(24)
    pf.space_after = Pt(12)
    pf.first_line_indent = Cm(0)
    pf.line_spacing = LINE_SPACING
    p.style = doc.styles['Heading 1']
    for r in p.runs:
        r.font.name = FONT_NAME
        r.font.size = Pt(HEADING1_SIZE)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0, 0, 0)
    return p


def add_subheading(doc, text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.name = FONT_NAME
    run.font.size = Pt(SUBHEADING_SIZE)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0, 0, 0)
    pf = p.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf.space_before = Pt(18)
    pf.space_after = Pt(8)
    pf.first_line_indent = Cm(0)
    pf.line_spacing = LINE_SPACING
    p.style = doc.styles['Heading 2']
    for r in p.runs:
        r.font.name = FONT_NAME
        r.font.size = Pt(SUBHEADING_SIZE)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0, 0, 0)
    return p


def add_page_break(doc):
    p = doc.add_paragraph()
    run = p.add_run()
    br_elem = parse_xml('<w:br %s w:type="page"/>' % nsdecls('w'))
    run._element.append(br_elem)
    return p


def add_bullet_point(doc, text):
    p = doc.add_paragraph(style='List Bullet')
    p.clear()
    run = p.add_run(text)
    run.font.name = FONT_NAME
    run.font.size = Pt(BODY_SIZE)
    run.font.color.rgb = RGBColor(0, 0, 0)
    pf = p.paragraph_format
    pf.line_spacing = LINE_SPACING
    pf.space_after = Pt(3)
    pf.first_line_indent = Cm(0)
    return p


def add_table(doc, title, headers, rows):
    cap = add_formatted_paragraph(doc, title, bold=True, font_size=BODY_SIZE,
                                   alignment=WD_ALIGN_PARAGRAPH.CENTER,
                                   first_line_indent=False, space_after=Pt(4),
                                   space_before=Pt(12))
    num_cols = len(headers)
    num_rows = len(rows) + 1
    table = doc.add_table(rows=num_rows, cols=num_cols)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = 'Table Grid'
    for ci, header in enumerate(headers):
        cell = table.rows[0].cells[ci]
        cell.text = ""
        p = cell.paragraphs[0]
        run = p.add_run(header)
        run.font.name = FONT_NAME
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0, 0, 0)
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        shading = parse_xml('<w:shd %s w:fill="D9E2F3" w:val="clear"/>' % nsdecls('w'))
        cell._element.get_or_add_tcPr().append(shading)
    for ri, row_data in enumerate(rows):
        for ci, cell_text in enumerate(row_data):
            cell = table.rows[ri + 1].cells[ci]
            cell.text = ""
            p = cell.paragraphs[0]
            run = p.add_run(str(cell_text))
            run.font.name = FONT_NAME
            run.font.size = Pt(11)
            run.font.color.rgb = RGBColor(0, 0, 0)
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    add_formatted_paragraph(doc, "", first_line_indent=False, space_after=Pt(6))


def setup_page_layout(section):
    section.top_margin = Cm(TOP_MARGIN)
    section.bottom_margin = Cm(BOTTOM_MARGIN)
    section.left_margin = Cm(LEFT_MARGIN)
    section.right_margin = Cm(RIGHT_MARGIN)


def add_footer(section, book_title):
    footer = section.footer
    footer.is_linked_to_previous = False
    for p in footer.paragraphs:
        p.clear()
    footer_p = footer.paragraphs[0]
    footer_p.clear()
    pPr = footer_p._element.get_or_add_pPr()
    tabs = parse_xml('<w:tabs %s><w:tab w:val="right" w:pos="9360"/></w:tabs>' % nsdecls('w'))
    pPr.append(tabs)
    run_pn = footer_p.add_run()
    run_pn._element.append(parse_xml('<w:fldChar %s w:fldCharType="begin"/>' % nsdecls('w')))
    run_pn2 = footer_p.add_run()
    run_pn2._element.append(parse_xml('<w:instrText %s xml:space="preserve"> PAGE </w:instrText>' % nsdecls('w')))
    run_pn3 = footer_p.add_run()
    run_pn3._element.append(parse_xml('<w:fldChar %s w:fldCharType="end"/>' % nsdecls('w')))
    footer_p.add_run("\t")
    run_title = footer_p.add_run(book_title[:80])
    run_title.font.name = FONT_NAME
    run_title.font.size = Pt(9)
    run_title.font.color.rgb = RGBColor(128, 128, 128)
    run_title.font.italic = True
    for run in [run_pn, run_pn2, run_pn3]:
        run.font.name = FONT_NAME
        run.font.size = Pt(9)
        run.font.color.rgb = RGBColor(128, 128, 128)


def main():
    print("Loading manuscript for final expansion...")
    doc = Document("sample_manuscript.docx")

    # ========================================
    # APPENDIX D: Architecture Blueprints
    # ========================================
    print("Adding Appendix D: Architecture Blueprints...")
    add_page_break(doc)
    add_heading1(doc, "Appendix D: Self-Evolving Architecture Blueprints")

    add_formatted_paragraph(doc, "This appendix presents detailed architecture blueprints for implementing self-evolving enterprise systems across different scales and complexity levels. Each blueprint provides a reference architecture that organizations can adapt to their specific needs, along with implementation guidance and technology recommendations.")

    add_subheading(doc, "D.1 Small-Scale Self-Evolving System Blueprint")
    add_formatted_paragraph(doc, "The small-scale blueprint is designed for organizations with up to 50 microservices, a single cloud provider, and a team of 10 to 30 engineers. This architecture provides the foundational capabilities of self-evolution including automated monitoring, basic self-healing, and initial AI-driven optimization. The architecture centers on a managed Kubernetes cluster with a service mesh for inter-service communication. A centralized observability platform collects metrics, logs, and traces from all services, feeding an AI analytics engine that identifies anomalies and suggests optimizations.")
    add_formatted_paragraph(doc, "The data layer consists of a combination of managed relational databases for transactional workloads and a data warehouse for analytics. A simple event streaming platform handles asynchronous communication between services. The AI/ML layer includes a managed ML platform for model training and deployment, with a model registry for version control and a feature store for reusable features. Security is implemented through a zero-trust gateway that handles authentication and authorization for all service-to-service and external communication.")
    add_formatted_paragraph(doc, "The self-evolving capabilities in this blueprint focus on three areas: automated scaling based on predicted load patterns, self-healing through health checks and automatic restart policies, and AI-assisted incident detection and alerting. The system uses a simple feedback loop where operational metrics are continuously analyzed by ML models that generate recommendations for configuration changes. These changes are reviewed by human operators before being applied, following a human-on-the-loop model.")
    add_formatted_paragraph(doc, "Key technologies recommended for this blueprint include Kubernetes (managed service), Istio or Linkerd for service mesh, Prometheus and Grafana for monitoring, Elasticsearch and Kibana for log management, Apache Kafka or managed alternatives for event streaming, and a cloud provider's managed ML platform (SageMaker, Azure ML, or Vertex AI) for AI capabilities. The estimated time to implement this blueprint is 6 to 12 months, depending on the organization's current maturity level.")

    add_subheading(doc, "D.2 Medium-Scale Self-Evolving System Blueprint")
    add_formatted_paragraph(doc, "The medium-scale blueprint is designed for organizations with 50 to 500 microservices, potentially spanning multiple cloud providers or hybrid environments, with teams of 30 to 150 engineers. This architecture extends the small-scale blueprint with more sophisticated AI capabilities, multi-region deployment, and advanced data management.")
    add_formatted_paragraph(doc, "The architecture introduces a dedicated AI orchestration layer that manages multiple ML models for different operational tasks. A knowledge graph captures relationships between services, infrastructure components, and business processes, enabling the system to reason about the impact of changes across the entire architecture. The data fabric layer provides unified access to data across multiple sources, with automated data quality monitoring and governance controls.")
    add_formatted_paragraph(doc, "Self-evolving capabilities in this blueprint include predictive auto-scaling using causal AI models, automated capacity planning based on business forecasts, AI-driven root cause analysis for incidents, automated remediation for known failure patterns, and intelligent traffic management with AI-powered canary analysis. The system operates in a hybrid human-on-the-loop and human-out-of-the-loop model, where routine optimizations are applied automatically while significant changes require human approval.")
    add_formatted_paragraph(doc, "This blueprint introduces several additional technologies including a graph database for the knowledge graph, a vector database for semantic search capabilities, a chaos engineering platform for resilience testing, an AIOps platform for intelligent operations, and a FinOps platform for cost optimization. Multi-cloud management tools and a centralized identity platform are also introduced to handle the increased complexity. The estimated implementation time is 12 to 24 months.")

    add_subheading(doc, "D.3 Large-Scale Self-Evolving System Blueprint")
    add_formatted_paragraph(doc, "The large-scale blueprint is designed for enterprise organizations with 500 or more microservices, global multi-cloud deployments, and teams of 150 or more engineers. This architecture represents the most sophisticated level of self-evolution, with fully autonomous operations for routine tasks and comprehensive AI governance.")
    add_formatted_paragraph(doc, "The architecture features a hierarchical AI management system with specialized agents for different operational domains including performance optimization, security monitoring, cost management, compliance enforcement, and capacity planning. These agents coordinate through a central orchestration layer that resolves conflicts and ensures consistency across the enterprise. A digital twin of the entire infrastructure enables the system to simulate changes before applying them to production.")
    add_formatted_paragraph(doc, "Advanced self-evolving capabilities in this blueprint include autonomous architecture optimization where the system can propose and implement changes to the microservice topology, AI-driven technical debt identification and resolution, automated compliance monitoring and enforcement across multiple regulatory frameworks, generative AI for code and configuration synthesis, and reinforcement learning agents that continuously optimize resource allocation and traffic routing.")
    add_formatted_paragraph(doc, "This blueprint requires a comprehensive technology stack including advanced AI/ML platforms with custom model training capabilities, a digital twin platform, a comprehensive governance and audit framework, multi-cloud orchestration with intelligent workload placement, edge computing infrastructure for distributed AI inference, and specialized hardware accelerators (GPUs, TPUs) for AI workloads. The estimated implementation time is 24 to 48 months, with continuous evolution thereafter.")

    add_subheading(doc, "D.4 Edge-First Self-Evolving System Blueprint")
    add_formatted_paragraph(doc, "The edge-first blueprint is designed for organizations where significant computation must occur at the edge, such as manufacturing, retail, healthcare, and IoT-intensive industries. This architecture distributes AI capabilities across a continuum from edge devices to fog nodes to cloud data centers, with each tier handling appropriate levels of intelligence.")
    add_formatted_paragraph(doc, "At the edge tier, lightweight ML models handle real-time inference for latency-sensitive tasks such as quality inspection, anomaly detection, and local control loops. The fog tier, typically consisting of on-premise servers or regional edge facilities, hosts more complex models for pattern recognition, local optimization, and data aggregation. The cloud tier handles model training, global optimization, and long-term analytics.")
    add_formatted_paragraph(doc, "Self-evolving capabilities in this blueprint focus on autonomous model deployment from cloud to edge, where the system automatically selects, compresses, and deploys the most appropriate model version for each edge device based on its capabilities and requirements. The system monitors model performance at each tier and automatically triggers retraining when drift is detected. Network-aware optimization ensures that data movement between tiers is minimized while maintaining model accuracy.")
    add_formatted_paragraph(doc, "Key technologies for this blueprint include edge AI frameworks such as TensorFlow Lite, ONNX Runtime, and Apache TVM for model optimization and deployment. Edge orchestration platforms handle the lifecycle management of edge devices and applications. Federated learning capabilities enable model improvement across distributed edge locations without centralizing sensitive data. The architecture also includes offline operation capabilities, ensuring that edge devices can continue to function intelligently even when connectivity to the cloud is disrupted.")

    # ========================================
    # APPENDIX E: Enterprise AI Maturity Model
    # ========================================
    print("Adding Appendix E: Enterprise AI Maturity Model...")
    add_page_break(doc)
    add_heading1(doc, "Appendix E: Enterprise AI Maturity Model")

    add_formatted_paragraph(doc, "The Enterprise AI Maturity Model provides a structured framework for organizations to assess their current level of AI adoption and chart a path toward fully self-evolving enterprise systems. The model defines five levels of maturity, each building upon the capabilities of the previous level. Organizations can use this model to identify their current position, set realistic goals for advancement, and prioritize investments in technology, people, and processes.")

    add_subheading(doc, "E.1 Level 1: AI Aware")
    add_formatted_paragraph(doc, "At Level 1, the organization has recognized the potential of AI for enterprise operations but has not yet implemented significant AI capabilities. Activities at this level include executive education on AI possibilities, initial assessment of AI use cases, and evaluation of available tools and platforms. The organization may have a few experimental AI projects or proof-of-concepts, but these are isolated efforts that have not been integrated into core operations.")
    add_formatted_paragraph(doc, "Key characteristics of Level 1 organizations include manual monitoring and operations with no AI assistance, rule-based automation using traditional scripts and scheduling, reactive incident response with manual investigation and resolution, static infrastructure with capacity provisioned based on peak estimates, and data stored in silos with limited cross-functional visibility. The primary challenge at this level is building organizational awareness and securing executive sponsorship for AI-driven transformation initiatives.")
    add_formatted_paragraph(doc, "To advance beyond Level 1, organizations should focus on establishing a data strategy that consolidates and cleanses operational data, building a small AI team or center of excellence, identifying two or three high-impact AI use cases for initial implementation, investing in observability infrastructure to generate the data needed for AI, and creating an AI governance framework that will guide future development. The typical duration at this level is 6 to 12 months for organizations committed to advancement.")

    add_subheading(doc, "E.2 Level 2: AI Assisted")
    add_formatted_paragraph(doc, "At Level 2, the organization has deployed AI tools that assist human operators in their work. AI provides recommendations and insights, but all decisions and actions are taken by human operators. The organization has established basic data pipelines and has begun to build the infrastructure needed for ML operations.")
    add_formatted_paragraph(doc, "Key characteristics of Level 2 organizations include AI-powered dashboards and alerts that highlight anomalies and potential issues, ML models that predict resource utilization and suggest scaling actions, AI-assisted incident triage that categorizes and prioritizes alerts, automated data collection and preparation for ML model training, and initial implementation of CI/CD pipelines for ML models. At this level, AI serves as an intelligent advisor, augmenting human decision-making without replacing it.")
    add_formatted_paragraph(doc, "The primary challenges at Level 2 include ensuring the quality and reliability of AI recommendations, building trust between human operators and AI systems, managing the increasing volume of data generated by observability tools, and developing the skills needed to build and maintain ML models in production. Organizations should invest in MLOps capabilities, expand their AI team, and begin to formalize governance processes for AI-driven recommendations.")

    add_subheading(doc, "E.3 Level 3: AI Augmented")
    add_formatted_paragraph(doc, "At Level 3, AI systems actively participate in operational tasks, with human operators providing oversight and handling exceptions. The organization has established robust MLOps practices and has deployed multiple AI models in production. Automated actions are taken for well-understood scenarios, while novel situations are escalated to human operators.")
    add_formatted_paragraph(doc, "Key characteristics of Level 3 organizations include automated scaling based on predictive models with human oversight, AI-driven incident response that automatically applies known remediations, automated configuration management with AI-optimized parameters, continuous model monitoring and automated retraining pipelines, integrated observability with AI-powered root cause analysis, and initial implementation of chaos engineering for resilience testing.")
    add_formatted_paragraph(doc, "The governance model at this level shifts to human-on-the-loop, where human operators monitor AI actions and can intervene if necessary. This requires well-defined escalation procedures, comprehensive audit logging, and regular review of AI-driven decisions to ensure alignment with organizational goals and policies. Organizations at this level should invest in building digital twins for testing AI-driven changes, expanding AI capabilities to cover more operational domains, and developing the organizational trust and processes needed for greater autonomy.")

    add_subheading(doc, "E.4 Level 4: AI Driven")
    add_formatted_paragraph(doc, "At Level 4, AI systems manage the majority of operational tasks autonomously, with human operators focusing on strategic decisions, exception handling, and governance oversight. The organization has a mature AI platform with sophisticated capabilities including multi-model orchestration, reinforcement learning for optimization, and generative AI for code and configuration synthesis.")
    add_formatted_paragraph(doc, "Key characteristics of Level 4 organizations include fully autonomous scaling, self-healing, and performance optimization, AI-driven architecture decisions including service decomposition and technology selection, automated compliance monitoring and enforcement across multiple regulatory frameworks, sophisticated FinOps with AI-optimized cost management, advanced security operations with AI-driven threat detection and automated response, and digital twin-based simulation for testing changes before production deployment.")
    add_formatted_paragraph(doc, "The governance model at this level is primarily human-out-of-the-loop for routine operations, with well-defined boundaries beyond which human approval is required. The organization has established comprehensive AI governance structures including model review boards, ethics committees, and regular external audits. The primary challenge at this level is maintaining the human expertise needed to understand and oversee increasingly autonomous systems.")

    add_subheading(doc, "E.5 Level 5: Self-Evolving")
    add_formatted_paragraph(doc, "Level 5 represents the fully self-evolving enterprise, where systems continuously adapt and improve without explicit human instruction. The architecture itself evolves in response to changing business requirements, technology landscapes, and operational patterns. Human operators serve as goal-setters and strategic guides, while the system handles the full spectrum of operational, tactical, and even some strategic decisions within defined boundaries.")
    add_formatted_paragraph(doc, "Key characteristics of Level 5 organizations include autonomous architecture evolution with the system proposing and implementing structural changes, continuous learning from operational experience with knowledge transfer across systems, proactive identification and resolution of technical debt, self-optimizing data pipelines that adapt to changing data patterns and business needs, AI systems that can explain their decisions and reasoning in human-understandable terms, and collaborative intelligence where multiple AI agents coordinate to manage the entire enterprise platform.")
    add_formatted_paragraph(doc, "Achieving Level 5 requires not only sophisticated technology but also a mature organizational culture that trusts and supports autonomous operations. It requires comprehensive governance frameworks that can evolve alongside the technology, a workforce that understands AI at a deep level and can guide its strategic direction, and a commitment to continuous improvement and innovation. Very few organizations have reached Level 5 as of the writing of this book, but it represents the aspirational goal that drives the entire field of self-evolving enterprise architecture.")

    # Add maturity model table
    add_table(doc, "Table E.1: Enterprise AI Maturity Model Summary",
              ["Level", "Name", "AI Role", "Human Role", "Key Capability"],
              [
                  ["1", "AI Aware", "None", "Full control", "Awareness and planning"],
                  ["2", "AI Assisted", "Advisor", "Decision maker", "Recommendations and insights"],
                  ["3", "AI Augmented", "Operator", "Supervisor", "Automated routine actions"],
                  ["4", "AI Driven", "Manager", "Governor", "Autonomous operations"],
                  ["5", "Self-Evolving", "Autonomous", "Strategist", "Architecture evolution"],
              ])

    # ========================================
    # APPENDIX F: Recommended Reading and Resources
    # ========================================
    print("Adding Appendix F: Recommended Reading...")
    add_page_break(doc)
    add_heading1(doc, "Appendix F: Recommended Reading and Resources")

    add_subheading(doc, "F.1 Foundational Texts")
    foundational = [
        "Artificial Intelligence: A Modern Approach by Stuart Russell and Peter Norvig – The definitive textbook on AI, covering the full breadth of the field from search algorithms and knowledge representation to machine learning and natural language processing. Essential reading for anyone seeking to understand the theoretical foundations of the AI systems discussed throughout this book.",
        "Designing Data-Intensive Applications by Martin Kleppmann – A comprehensive guide to the principles and practices of building reliable, scalable, and maintainable data systems. This book provides the data architecture foundation needed for self-evolving systems, covering topics from replication and partitioning to stream processing and data integration.",
        "Deep Learning by Ian Goodfellow, Yoshua Bengio, and Aaron Courville – The authoritative textbook on deep learning, providing mathematical rigor and practical insights into the neural network architectures that power modern AI systems. Essential for understanding the models that drive autonomous decision-making in self-evolving platforms.",
        "Building Microservices by Sam Newman – A practical guide to designing and building microservices architectures, covering decomposition strategies, integration patterns, deployment, and testing. This book provides the architectural foundation for the distributed systems on which self-evolving architectures are built.",
        "Release It! by Michael Nygard – A guide to designing and deploying production-ready software, with extensive coverage of stability patterns, capacity patterns, and operational practices. The resilience patterns discussed in this book are directly applicable to building self-healing capabilities in self-evolving systems.",
    ]
    for item in foundational:
        add_bullet_point(doc, item)

    add_subheading(doc, "F.2 AI and Machine Learning")
    ai_reading = [
        "Designing Machine Learning Systems by Chip Huyen – A practical guide to the end-to-end process of building ML systems, from problem framing to monitoring in production. Particularly relevant for understanding the MLOps practices that enable self-evolving AI capabilities.",
        "Reinforcement Learning: An Introduction by Richard Sutton and Andrew Barto – The foundational textbook on reinforcement learning, covering the algorithms and theory behind RL agents. Essential reading for understanding how self-evolving systems learn to optimize their own behavior through interaction with their environment.",
        "Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow by Aurélien Géron – A practical guide to implementing ML algorithms using popular Python libraries. Provides the implementation knowledge needed to build the AI components of self-evolving systems.",
        "Natural Language Processing with Transformers by Lewis Tunstall, Leandro von Werra, and Thomas Wolf – A comprehensive guide to working with transformer models for NLP tasks, including practical guidance on fine-tuning and deploying large language models in enterprise settings.",
        "Trustworthy Machine Learning by Kush Varshney – An exploration of the challenges and techniques for building ML systems that are fair, robust, private, and interpretable. Critical reading for implementing the AI governance and ethics frameworks discussed in this book.",
    ]
    for item in ai_reading:
        add_bullet_point(doc, item)

    add_subheading(doc, "F.3 Cloud Architecture and Operations")
    cloud_reading = [
        "Cloud Native Patterns by Cornelia Davis – A guide to designing applications that fully exploit the advantages of cloud computing, covering patterns for scalability, resilience, and manageability. These patterns form the foundation for self-evolving cloud architectures.",
        "The Site Reliability Engineering series by Google (SRE Book, SRE Workbook, Building Secure and Reliable Systems) – Google's approach to managing large-scale production systems, covering principles of reliability, monitoring, incident response, and automation that are directly applicable to self-evolving operations.",
        "Kubernetes in Action by Marko Luksa – A detailed guide to the Kubernetes container orchestration platform, essential for understanding the infrastructure layer of self-evolving architectures.",
        "Observability Engineering by Charity Majors, Liz Fong-Jones, and George Miranda – A comprehensive guide to building observable systems, covering the tools, techniques, and cultural practices needed to understand the behavior of complex distributed systems. Essential for implementing the deep observability discussed in this book.",
        "Cloud FinOps by J.R. Storment and Mike Fuller – A guide to the financial management of cloud resources, covering the principles, practices, and cultural changes needed to optimize cloud spending. Relevant for the cost optimization aspects of cognitive resource management discussed in this book.",
    ]
    for item in cloud_reading:
        add_bullet_point(doc, item)

    add_subheading(doc, "F.4 Online Resources and Communities")
    online_resources = [
        "ArXiv (arxiv.org) – The preprint repository where cutting-edge AI and ML research papers are published. Following the cs.AI, cs.LG, and cs.DC categories provides early access to the research that drives innovation in self-evolving systems.",
        "Papers With Code (paperswithcode.com) – A repository linking ML papers with their implementation code, making it easier to understand and reproduce the latest research. An invaluable resource for staying current with advances in AI techniques.",
        "The CNCF Landscape (landscape.cncf.io) – A comprehensive map of the cloud-native computing ecosystem, maintained by the Cloud Native Computing Foundation. Useful for understanding the technology options available for building self-evolving infrastructure.",
        "Hugging Face (huggingface.co) – The leading platform for open-source ML models and datasets, with extensive documentation and community support. Essential for organizations working with NLP and generative AI.",
        "Google AI Blog, OpenAI Blog, Meta AI Blog, and similar – Official blogs from major AI research organizations that provide accessible explanations of new research and its potential applications in enterprise settings.",
    ]
    for item in online_resources:
        add_bullet_point(doc, item)

    # ========================================
    # ACKNOWLEDGMENTS (insert conceptually before chapters, but append here)
    # ========================================
    print("Adding Acknowledgments...")
    add_page_break(doc)
    add_heading1(doc, "Acknowledgments")

    ack_text = """Writing a comprehensive book on self-evolving enterprise systems has been a journey that would not have been possible without the support and contributions of many individuals and organizations. I owe a deep debt of gratitude to all who have helped shape the ideas, refine the content, and bring this book to completion.

First and foremost, I would like to thank the many practitioners, architects, and engineers who shared their experiences and insights with me during the research phase of this book. Their real-world perspectives on the challenges and opportunities of building AI-driven enterprise platforms have been invaluable in grounding the theoretical concepts in practical reality.

I am deeply grateful to the reviewers who invested their time and expertise in providing feedback on early drafts of the manuscript. Their critical comments, suggestions, and corrections have significantly improved the quality and accuracy of the final text. Any remaining errors or omissions are, of course, my own responsibility.

My thanks also go to the academic community, particularly the researchers working at the intersection of artificial intelligence, distributed systems, and software engineering. The theoretical foundations laid by their work form the backbone of the ideas presented in this book. I have endeavored to cite their contributions throughout the text and in the bibliography.

I would like to acknowledge the open-source community, whose tools and platforms have made it possible to build the kinds of systems described in this book. From Kubernetes and TensorFlow to Prometheus and Apache Kafka, the open-source ecosystem provides the building blocks for self-evolving enterprise architectures. The collaborative spirit of this community is a model for the kind of cooperation that will be needed to realize the vision of truly autonomous enterprise platforms.

Special thanks go to the publishing team at Eclearnix Edtech Private Limited for their professionalism, patience, and commitment to producing a high-quality publication. Their editorial guidance and production expertise have been essential in transforming the manuscript into the book you hold today.

Finally, I would like to thank my family and friends for their unwavering support and encouragement throughout the long process of writing this book. Their understanding during the many late nights and weekends spent at the keyboard has been a source of strength and motivation. This book is dedicated to them, and to all those who believe in the power of technology to create a better world.

The field of self-evolving enterprise systems is evolving rapidly, and I look forward to continuing this journey of exploration and discovery. I invite readers to share their experiences, questions, and feedback, as the conversation around autonomous enterprise platforms is one that benefits from diverse perspectives and collective wisdom."""

    for para in ack_text.strip().split('\n\n'):
        if para.strip():
            add_formatted_paragraph(doc, para.strip())

    # ========================================
    # APPENDIX G: Hands-On Exercises
    # ========================================
    print("Adding Appendix G: Hands-On Exercises...")
    add_page_break(doc)
    add_heading1(doc, "Appendix G: Hands-On Exercises and Lab Activities")

    add_formatted_paragraph(doc, "This appendix provides practical exercises and lab activities designed to reinforce the concepts presented in each chapter. These exercises are intended for individual study, classroom use, or team workshops. Each exercise includes learning objectives, prerequisites, step-by-step instructions, and expected outcomes.")

    exercises = [
        ("Exercise 1: Building a Self-Monitoring Microservice",
         "In this exercise, you will create a simple microservice that implements basic self-monitoring capabilities. The service will expose health check endpoints, emit structured metrics, and include a simple anomaly detection algorithm that monitors its own performance metrics. You will use Python with Flask for the web framework, Prometheus client library for metrics exposition, and a simple statistical model for anomaly detection. The exercise walks you through the process of defining key performance indicators, implementing metric collection, setting up baseline calculations, and creating alert conditions based on statistical deviations from normal behavior. By the end of this exercise, you will understand the foundational building blocks of self-monitoring systems and how they contribute to the broader goal of self-evolution."),

        ("Exercise 2: Implementing a Circuit Breaker Pattern",
         "This exercise guides you through the implementation of the circuit breaker resilience pattern in a distributed microservices environment. You will create two communicating services and implement a circuit breaker that protects the calling service from cascading failures when the downstream service becomes unhealthy. The exercise covers the three states of a circuit breaker (closed, open, half-open), the configuration of failure thresholds and recovery timeouts, and the integration of circuit breaker metrics with the monitoring system. You will also experiment with different failure scenarios and observe how the circuit breaker pattern prevents system-wide degradation."),

        ("Exercise 3: Setting Up a Basic ML Pipeline with MLOps",
         "In this exercise, you will establish a complete ML pipeline from data preparation to model deployment, following MLOps best practices. The exercise uses a simple predictive model that forecasts system load based on historical metrics. You will implement data versioning, experiment tracking, model training with hyperparameter tuning, model evaluation, and automated deployment to a model serving endpoint. The pipeline will include automated retraining triggers based on model performance degradation, demonstrating a fundamental capability of self-evolving systems."),

        ("Exercise 4: Building an AI-Powered Anomaly Detection System",
         "This exercise walks you through the development of an AI-powered anomaly detection system for monitoring enterprise applications. Using real-world server metrics data, you will implement and compare multiple anomaly detection approaches including statistical methods (Z-score, IQR), isolation forests, and autoencoders. The exercise covers data preprocessing, feature engineering, model training, threshold tuning, and integration with an alerting system. You will evaluate the trade-offs between different approaches in terms of detection accuracy, false positive rate, and computational cost."),

        ("Exercise 5: Implementing a Simple Reinforcement Learning Agent",
         "In this exercise, you will build a reinforcement learning agent that learns to optimize the scaling policy for a simulated web application. The environment simulates varying traffic patterns, and the RL agent must learn to scale the number of application instances to balance performance (response time) against cost (number of running instances). You will implement a Q-learning algorithm, design the state and action spaces, and define a reward function that captures the multi-objective optimization problem. The exercise demonstrates how RL can be applied to enterprise resource management decisions."),

        ("Exercise 6: Creating an Explainable AI Dashboard",
         "This exercise guides you through building an interactive dashboard that provides explanations for AI model predictions. Using a pre-trained classification model, you will implement LIME and SHAP explanations and display them in a web-based dashboard. The exercise covers the interpretation of feature importance, the creation of counterfactual explanations, and the design of user interfaces that effectively communicate AI reasoning to non-technical stakeholders. This demonstrates the explainability capabilities that are essential for governing self-evolving systems."),

        ("Exercise 7: Setting Up a Chaos Engineering Experiment",
         "In this exercise, you will design and execute a chaos engineering experiment to test the resilience of a distributed system. Using a containerized microservices application, you will inject different types of failures including network latency, pod termination, and CPU stress. The exercise covers hypothesis formulation, blast radius definition, experiment execution, and result analysis. You will observe how self-healing mechanisms respond to injected failures and identify weaknesses that need to be addressed in the system's resilience strategy."),

        ("Exercise 8: Building a Zero-Trust API Gateway",
         "This exercise walks you through the implementation of a zero-trust API gateway that authenticates and authorizes every request, regardless of its origin. You will implement JWT-based authentication, role-based access control, request rate limiting, and request logging for audit purposes. The exercise also covers the integration of the gateway with a centralized identity provider and the implementation of mutual TLS for service-to-service authentication. This demonstrates the security architecture that underpins autonomous enterprise systems."),

        ("Exercise 9: Implementing a Data Quality Monitoring Pipeline",
         "In this exercise, you will build an automated data quality monitoring pipeline that continuously validates data as it flows through the enterprise. Using Great Expectations or a similar framework, you will define data quality rules, implement automated data profiling, set up alerts for quality violations, and create a data quality dashboard. The exercise demonstrates how automated data quality monitoring supports the data-dependent decision-making capabilities of self-evolving systems."),

        ("Exercise 10: Building a Digital Twin for System Simulation",
         "This capstone exercise guides you through the creation of a simplified digital twin of an enterprise application. The digital twin simulates the behavior of the application under different load conditions and configuration parameters. You will use the digital twin to test hypothetical changes before applying them to the production system, demonstrating a key capability of Level 4 and Level 5 self-evolving architectures. The exercise covers system modeling, simulation execution, result comparison with actual system behavior, and the use of the digital twin for predictive analysis."),
    ]

    for title, description in exercises:
        add_subheading(doc, title)
        add_formatted_paragraph(doc, description)

    # ========================================
    # Update footers
    # ========================================
    print("Updating footers...")
    for section in doc.sections:
        setup_page_layout(section)
        add_footer(section, BOOK_TITLE)

    # Save
    print("Saving final document...")
    doc.save("sample_manuscript.docx")

    # Stats
    total_words = sum(len(p.text.split()) for p in doc.paragraphs if p.text.strip())
    estimated_pages = total_words // 250
    print("\n=== FINAL DOCUMENT STATISTICS ===")
    print("Total paragraphs: %d" % len(doc.paragraphs))
    print("Total words: %d" % total_words)
    print("Estimated pages: %d" % estimated_pages)
    print("Tables: %d" % len(doc.tables))
    print("\nDocument saved successfully!")


if __name__ == "__main__":
    main()
