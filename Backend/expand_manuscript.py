"""
Expand the existing sample_manuscript.docx by adding:
- Glossary section
- Additional 'Discussion Questions' sections per chapter  
- Extended chapter summaries
- Additional review content
- Bibliography/References section
This will add ~20,000 more words to reach ~500 pages.
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
    if first_line_indent:
        pf.first_line_indent = Cm(FIRST_LINE_INDENT_CM)
    else:
        pf.first_line_indent = Cm(0)
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
    tabs = parse_xml(
        '<w:tabs %s>'
        '  <w:tab w:val="right" w:pos="9360"/>'
        '</w:tabs>' % nsdecls('w')
    )
    pPr.append(tabs)
    run_pn = footer_p.add_run()
    fldChar1 = parse_xml('<w:fldChar %s w:fldCharType="begin"/>' % nsdecls('w'))
    run_pn._element.append(fldChar1)
    run_pn2 = footer_p.add_run()
    instrText = parse_xml('<w:instrText %s xml:space="preserve"> PAGE </w:instrText>' % nsdecls('w'))
    run_pn2._element.append(instrText)
    run_pn3 = footer_p.add_run()
    fldChar2 = parse_xml('<w:fldChar %s w:fldCharType="end"/>' % nsdecls('w'))
    run_pn3._element.append(fldChar2)
    run_tab = footer_p.add_run("\t")
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
    print("Loading existing manuscript...")
    doc = Document("sample_manuscript.docx")

    # ========================================
    # Add expanded chapter review sections and additional content
    # We insert these BEFORE the Index (which is the last heading)
    # ========================================

    # Find the Index heading position - we'll add new content at the end
    # Actually, it's easier to just append to the document and then re-add the index
    # Instead, let's just add new sections at the end of the document

    print("Adding Glossary section...")
    add_page_break(doc)
    add_heading1(doc, "Glossary of Terms")

    glossary_terms = [
        ("Abstraction Layer", "A software layer that hides the complexity of underlying systems, providing a simplified interface for interaction. In self-evolving systems, abstraction layers allow AI components to interact with diverse infrastructure without needing to understand the specific details of each platform or service. This concept is fundamental to building portable and maintainable architectures that can adapt to changing technology landscapes."),
        ("Agent-Based System", "A computational system composed of autonomous agents that can perceive their environment, make decisions, and take actions to achieve specific goals. In enterprise AI, agent-based systems enable distributed problem-solving where multiple AI agents collaborate to manage different aspects of system operations, from resource allocation to security monitoring and performance optimization."),
        ("Anomaly Detection", "The identification of patterns in data that do not conform to expected behavior. In self-evolving systems, anomaly detection algorithms continuously monitor system metrics, user behavior, and data flows to identify potential issues before they become critical. Machine learning techniques such as isolation forests, autoencoders, and statistical process control are commonly used for this purpose."),
        ("Autonomous Computing", "A computing paradigm where systems can manage themselves with minimal human intervention. Inspired by the autonomic nervous system in biology, autonomous computing systems implement self-configuration, self-healing, self-optimization, and self-protection. This concept forms the backbone of self-evolving enterprise architectures."),
        ("Backpropagation", "A fundamental algorithm in neural network training that calculates the gradient of the loss function with respect to each weight in the network. By propagating error signals backward through the network layers, backpropagation enables the network to learn by adjusting weights to minimize prediction errors. This algorithm is essential for training the deep learning models used in enterprise AI systems."),
        ("Batch Processing", "A method of processing data where a collection of data is gathered over a period of time and then processed all at once. While batch processing is being supplemented by real-time streaming in many enterprise applications, it remains important for tasks such as model training, large-scale analytics, and periodic report generation in self-evolving systems."),
        ("Canary Deployment", "A deployment strategy where a new version of a service is gradually rolled out to a small subset of users before being deployed to the entire infrastructure. In self-evolving systems, AI algorithms can automatically manage canary deployments by monitoring key performance indicators and deciding whether to proceed with the full rollout or roll back to the previous version."),
        ("Cognitive Computing", "An approach to computing that aims to simulate human thought processes in a computerized model. Cognitive systems use machine learning, natural language processing, and other AI techniques to understand, reason, and learn from data. In the enterprise context, cognitive computing enables systems that can process unstructured data, understand context, and make nuanced decisions."),
        ("Container Orchestration", "The automated management of containerized applications across multiple hosts. Container orchestration platforms like Kubernetes handle deployment, scaling, networking, and availability of containers. In self-evolving systems, AI-enhanced orchestration goes beyond basic scheduling to implement intelligent placement, proactive scaling, and self-healing capabilities."),
        ("Data Drift", "A change in the statistical properties of the data that a machine learning model receives in production compared to the data it was trained on. Data drift is a critical concern in self-evolving systems because it can cause model accuracy to degrade over time. Automated drift detection and model retraining are essential capabilities for maintaining system intelligence."),
        ("Data Gravity", "The concept that as data accumulates in a particular location, it tends to attract more data, services, and applications to that location. Data gravity is an important consideration in resource optimization for self-evolving systems, as it affects decisions about where to place computational resources and how to manage data movement between cloud regions and edge locations."),
        ("Data Lineage", "The tracking and documentation of the complete lifecycle of data as it moves through various systems, transformations, and processes. Data lineage is critical for governance, compliance, and debugging in self-evolving systems. It enables architects to understand the provenance of data used in AI decision-making and to trace the impact of changes across the data pipeline."),
        ("Digital Twin", "A virtual representation of a physical system, process, or entity that is continuously updated with real-time data. In self-evolving enterprise systems, digital twins can be used to simulate the behavior of the entire IT infrastructure, allowing the system to test potential optimizations in a safe virtual environment before applying them to the live system."),
        ("Distributed Consensus", "A process by which multiple nodes in a distributed system agree on a single value or state. Consensus algorithms such as Raft, Paxos, and Byzantine Fault Tolerance are essential for maintaining consistency in self-evolving systems where multiple AI agents may need to coordinate their actions across a distributed infrastructure."),
        ("Edge Computing", "A computing paradigm that brings data processing closer to the source of data generation, reducing latency and bandwidth usage. In self-evolving systems, edge computing enables real-time AI inference at the point of data collection, which is critical for applications such as IoT, autonomous vehicles, and real-time security monitoring."),
        ("Embedding", "A numerical representation of data, typically in a high-dimensional vector space, that captures semantic relationships. Embeddings are used extensively in self-evolving systems for similarity search, recommendation engines, and natural language understanding. The quality of embeddings directly affects the system's ability to understand and reason about its operational context."),
        ("Feature Engineering", "The process of using domain knowledge to create input variables (features) that improve the performance of machine learning models. In self-evolving systems, feature engineering is increasingly automated through techniques such as automated feature stores, feature selection algorithms, and representation learning."),
        ("Fitness Function", "A mathematical function that evaluates how well a candidate solution meets the desired objectives. In self-evolving architectures, fitness functions are used to guide autonomous optimization by defining the criteria that the system should optimize for, such as performance, cost, reliability, and security."),
        ("Gradient Descent", "An optimization algorithm used to minimize the loss function in machine learning by iteratively adjusting model parameters in the direction of steepest descent. Variants such as stochastic gradient descent, Adam, and RMSprop are used to train the neural networks that power the intelligence in self-evolving enterprise systems."),
        ("Horizontal Scaling", "The process of adding more machines to a system to handle increased load, as opposed to vertical scaling which adds more power to existing machines. Self-evolving systems use AI-driven horizontal scaling to automatically adjust the number of service instances based on predicted demand patterns and current system conditions."),
        ("Hyperparameter Tuning", "The process of optimizing the configuration parameters of a machine learning algorithm that are not learned from data. In self-evolving systems, automated hyperparameter tuning techniques such as Bayesian optimization, random search, and population-based training are used to continuously improve model performance without human intervention."),
        ("Idempotency", "The property of an operation where performing it multiple times produces the same result as performing it once. Idempotency is a critical design principle in self-evolving systems, particularly for self-healing mechanisms where retry logic must be able to safely re-execute operations without causing unintended side effects."),
        ("Inference Pipeline", "The series of steps involved in using a trained machine learning model to make predictions on new data. In self-evolving systems, inference pipelines must be optimized for latency, throughput, and cost. AI-driven optimization of inference pipelines is a key capability, including techniques such as model compilation, quantization, and batching."),
        ("Knowledge Distillation", "A technique where a smaller, more efficient model is trained to replicate the behavior of a larger, more complex model. Knowledge distillation is particularly important in self-evolving systems for deploying AI capabilities to resource-constrained edge devices while maintaining acceptable accuracy levels."),
        ("Latent Space", "The abstract, lower-dimensional representation of data learned by a neural network. In self-evolving systems, latent space representations enable the system to understand complex relationships in operational data, detect anomalies, and generate synthetic data for testing and simulation purposes."),
        ("Model Serving", "The process of deploying a trained machine learning model to a production environment where it can receive requests and return predictions. Model serving infrastructure in self-evolving systems must support features such as A/B testing, traffic splitting, automatic rollback, and dynamic model switching based on real-time performance metrics."),
        ("Neuromorphic Computing", "A computing architecture inspired by the structure and function of biological neural networks. Neuromorphic chips process information using spiking neural networks that operate more like biological neurons, potentially offering significant advantages in energy efficiency and real-time processing for edge AI applications in self-evolving systems."),
        ("Observability", "The ability to understand the internal state of a system by examining its outputs, including metrics, logs, traces, and profiles. In self-evolving systems, observability is the foundation of autonomous operation, providing the data that AI algorithms need to monitor, diagnose, and optimize system behavior."),
        ("Prompt Engineering", "The practice of designing and optimizing the text inputs given to large language models to elicit desired outputs. In self-evolving systems, automated prompt engineering and prompt optimization are emerging capabilities that allow the system to improve its own interactions with LLMs over time."),
        ("Quantum Machine Learning", "The intersection of quantum computing and machine learning, where quantum algorithms are used to accelerate or improve machine learning tasks. While still largely theoretical for enterprise applications, quantum machine learning has the potential to revolutionize optimization problems in self-evolving systems."),
        ("Retrieval-Augmented Generation (RAG)", "An AI technique that combines information retrieval with text generation, allowing a language model to access external knowledge bases to provide more accurate and contextual responses. RAG is increasingly used in self-evolving systems for intelligent documentation, automated support, and context-aware decision-making."),
        ("Semantic Search", "A search technique that understands the intent and contextual meaning of a query rather than just matching keywords. Semantic search, powered by vector embeddings and similarity algorithms, enables self-evolving systems to find relevant information across large and diverse knowledge bases, improving both automated decision-making and human-AI collaboration."),
        ("Service Level Objective (SLO)", "A target value or range of values for a service level indicator that defines the desired reliability of a service. In self-evolving systems, SLOs serve as key inputs to fitness functions, guiding autonomous optimization to ensure that system performance meets business requirements while minimizing cost."),
        ("Synthetic Data", "Artificially generated data that mimics the statistical properties of real data. In self-evolving systems, synthetic data is used for testing new configurations, training AI models when real data is scarce or sensitive, and simulating failure scenarios for chaos engineering experiments."),
        ("Technical Debt", "The implied cost of rework caused by choosing expedient solutions over better approaches in software development. Self-evolving systems can help manage technical debt by automatically identifying, prioritizing, and in some cases resolving code quality issues, configuration drift, and architectural anti-patterns."),
        ("Tensor Processing Unit (TPU)", "A specialized hardware accelerator designed by Google for machine learning workloads, particularly neural network training and inference. TPUs, along with GPUs and other AI accelerators, provide the computational foundation for the AI capabilities in self-evolving enterprise systems."),
        ("Zero Trust Architecture", "A security model based on the principle that no user or system should be automatically trusted, regardless of their location within or outside the network perimeter. In self-evolving systems, zero trust is implemented through continuous verification, least-privilege access, and AI-driven threat detection."),
    ]

    for term, definition in glossary_terms:
        p = doc.add_paragraph()
        run_term = p.add_run(term + ": ")
        run_term.font.name = FONT_NAME
        run_term.font.size = Pt(BODY_SIZE)
        run_term.font.bold = True
        run_term.font.color.rgb = RGBColor(0, 0, 0)
        run_def = p.add_run(definition)
        run_def.font.name = FONT_NAME
        run_def.font.size = Pt(BODY_SIZE)
        run_def.font.color.rgb = RGBColor(0, 0, 0)
        pf = p.paragraph_format
        pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        pf.line_spacing = LINE_SPACING
        pf.first_line_indent = Cm(0)
        pf.space_after = Pt(8)
        pf.space_before = Pt(4)

    # ========================================
    # BIBLIOGRAPHY / REFERENCES
    # ========================================
    print("Adding Bibliography section...")
    add_page_break(doc)
    add_heading1(doc, "Bibliography and References")

    references = [
        "Amodei, D., Olah, C., Steinhardt, J., Christiano, P., Schulman, J., and Mané, D. (2016). Concrete Problems in AI Safety. arXiv preprint arXiv:1606.06565.",
        "Bahdanau, D., Cho, K., and Bengio, Y. (2015). Neural Machine Translation by Jointly Learning to Align and Translate. Proceedings of the International Conference on Learning Representations (ICLR).",
        "Bernstein, P., Hadzilacos, V., and Goodman, N. (1987). Concurrency Control and Recovery in Database Systems. Addison-Wesley.",
        "Brown, T., Mann, B., Ryder, N., et al. (2020). Language Models are Few-Shot Learners. Advances in Neural Information Processing Systems, 33, 1877-1901.",
        "Burns, B., Grant, B., Oppenheimer, D., Brewer, E., and Wilkes, J. (2016). Borg, Omega, and Kubernetes. ACM Queue, 14(1), 70-93.",
        "Chollet, F. (2018). Deep Learning with Python. Manning Publications.",
        "Dean, J. and Ghemawat, S. (2008). MapReduce: Simplified Data Processing on Large Clusters. Communications of the ACM, 51(1), 107-113.",
        "Devlin, J., Chang, M., Lee, K., and Toutanova, K. (2019). BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding. Proceedings of NAACL-HLT, 4171-4186.",
        "Evans, E. (2003). Domain-Driven Design: Tackling Complexity in the Heart of Software. Addison-Wesley Professional.",
        "Fowler, M. and Lewis, J. (2014). Microservices: A Definition of This New Architectural Term. martinfowler.com.",
        "Gamma, E., Helm, R., Johnson, R., and Vlissides, J. (1994). Design Patterns: Elements of Reusable Object-Oriented Software. Addison-Wesley.",
        "Goodfellow, I., Bengio, Y., and Courville, A. (2016). Deep Learning. MIT Press.",
        "Hamilton, J. (2007). On Designing and Deploying Internet-Scale Services. Proceedings of the 21st Large Installation System Administration Conference (LISA), 231-244.",
        "He, K., Zhang, X., Ren, S., and Sun, J. (2016). Deep Residual Learning for Image Recognition. Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 770-778.",
        "Hochreiter, S. and Schmidhuber, J. (1997). Long Short-Term Memory. Neural Computation, 9(8), 1735-1780.",
        "Huyen, C. (2022). Designing Machine Learning Systems. O'Reilly Media.",
        "Kephart, J. and Chess, D. (2003). The Vision of Autonomic Computing. IEEE Computer, 36(1), 41-50.",
        "Kleppmann, M. (2017). Designing Data-Intensive Applications: The Big Ideas Behind Reliable, Scalable, and Maintainable Systems. O'Reilly Media.",
        "Kratzke, N. and Quint, P. (2017). Understanding Cloud-Native Applications After 10 Years of Cloud Computing. Journal of Systems and Software, 126, 1-16.",
        "LeCun, Y., Bengio, Y., and Hinton, G. (2015). Deep Learning. Nature, 521(7553), 436-444.",
        "Lewis, M. and Li, S. (2019). Serverless Computing: Design Patterns and Best Practices. Addison-Wesley Professional.",
        "Lundberg, S. and Lee, S. (2017). A Unified Approach to Interpreting Model Predictions. Advances in Neural Information Processing Systems, 30.",
        "McMahan, B., Moore, E., Ramage, D., Hampson, S., and Aguera y Arcas, B. (2017). Communication-Efficient Learning of Deep Networks from Decentralized Data. Proceedings of AISTATS.",
        "Mnih, V., Kavukcuoglu, K., Silver, D., et al. (2015). Human-Level Control Through Deep Reinforcement Learning. Nature, 518(7540), 529-533.",
        "Newman, S. (2021). Building Microservices: Designing Fine-Grained Systems, 2nd Edition. O'Reilly Media.",
        "Nygard, M. (2018). Release It! Design and Deploy Production-Ready Software, 2nd Edition. Pragmatic Bookshelf.",
        "Paszke, A., Gross, S., Massa, F., et al. (2019). PyTorch: An Imperative Style, High-Performance Deep Learning Library. Advances in Neural Information Processing Systems, 32.",
        "Radford, A., Wu, J., Child, R., et al. (2019). Language Models are Unsupervised Multitask Learners. OpenAI Blog.",
        "Ribeiro, M., Singh, S., and Guestrin, C. (2016). 'Why Should I Trust You?' Explaining the Predictions of Any Classifier. Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining.",
        "Russell, S. and Norvig, P. (2021). Artificial Intelligence: A Modern Approach, 4th Edition. Pearson.",
        "Schulman, J., Wolski, F., Dhariwal, P., Radford, A., and Klimov, O. (2017). Proximal Policy Optimization Algorithms. arXiv preprint arXiv:1707.06347.",
        "Silver, D., Huang, A., Maddison, C., et al. (2016). Mastering the Game of Go with Deep Neural Networks and Tree Search. Nature, 529(7587), 484-489.",
        "Sutton, R. and Barto, A. (2018). Reinforcement Learning: An Introduction, 2nd Edition. MIT Press.",
        "Tanenbaum, A. and Van Steen, M. (2017). Distributed Systems: Principles and Paradigms, 3rd Edition. Pearson.",
        "Vaswani, A., Shazeer, N., Parmar, N., et al. (2017). Attention Is All You Need. Advances in Neural Information Processing Systems, 30.",
        "Vogels, W. (2009). Eventually Consistent. Communications of the ACM, 52(1), 40-44.",
        "Wolf, T., Debut, L., Sanh, V., et al. (2020). Transformers: State-of-the-Art Natural Language Processing. Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP), 38-45.",
        "Zaharia, M., Chowdhury, M., Franklin, M., Shenker, S., and Stoica, I. (2010). Spark: Cluster Computing with Working Sets. Proceedings of the 2nd USENIX Workshop on Hot Topics in Cloud Computing.",
        "Zhang, T., Patil, S., Goyal, N., et al. (2022). OPT: Open Pre-trained Transformer Language Models. arXiv preprint arXiv:2205.01068.",
        "Zhu, X., Goldberg, A. (2009). Introduction to Semi-Supervised Learning. Synthesis Lectures on Artificial Intelligence and Machine Learning. Morgan and Claypool Publishers.",
    ]

    for ri, ref in enumerate(references):
        ref_text = "[%d] %s" % (ri + 1, ref)
        add_formatted_paragraph(doc, ref_text, font_size=11,
                                alignment=WD_ALIGN_PARAGRAPH.LEFT,
                                first_line_indent=False, space_after=Pt(6))

    # ========================================
    # APPENDIX A: Discussion Questions by Chapter
    # ========================================
    print("Adding Appendix A: Discussion Questions...")
    add_page_break(doc)
    add_heading1(doc, "Appendix A: Discussion Questions")

    chapter_titles = [
        "The Dawn of Self-Evolving Systems",
        "From Monoliths to Intelligent Mesh",
        "Technological Foundations of AI-Driven Platforms",
        "Cognitive Resource Management and Optimization",
        "Engineering Resilience: Self-Healing and Autonomy",
        "Generative Architectures: AI-Assisted Schema and Code",
        "The Intelligent Data Fabric",
        "Reinforcement Learning for Continuous Improvement",
        "Securing the Autonomous Perimeter",
        "Explainable AI and Deep Observability",
        "Scaling the Self-Evolving Enterprise",
        "AIOps: Reimagining the Software Lifecycle",
        "Governance, Ethics, and Human Agency",
        "Real-World Implementation and Case Studies",
        "The Horizon of Enterprise Intelligence",
    ]

    discussion_questions = {
        1: [
            "How does the concept of self-evolution in enterprise systems differ from traditional automated processes? Provide specific examples of where simple automation ends and self-evolution begins in the context of a modern enterprise.",
            "Discuss the biological metaphor of natural selection as applied to enterprise architecture. What are the strengths and limitations of this analogy? How might it mislead architects if taken too literally?",
            "Consider the ethical implications of systems that can modify their own behavior. What safeguards should be in place, and how do we balance the benefits of autonomous operation with the need for human control and oversight?",
            "Analyze the convergence of cloud computing, artificial intelligence, and big data as enablers of self-evolving systems. Which of these three technologies do you consider the most critical catalyst, and why?",
            "How should organizations prepare their existing workforce for the transition to self-evolving systems? Discuss the new skills, roles, and cultural changes that are necessary for successful adoption.",
        ],
        2: [
            "Compare and contrast the monolithic, microservices, and intelligent mesh architectural patterns. Under what circumstances might a monolithic architecture still be the best choice for an organization?",
            "Discuss the challenges of migrating from a monolithic architecture to an intelligent mesh. What strategies can minimize risk during this transition, and how does the strangler fig pattern help?",
            "How does the service mesh abstraction change the way developers think about cross-cutting concerns such as security, observability, and resilience? What are the trade-offs of delegating these concerns to infrastructure?",
            "Analyze the role of event-driven architecture in enabling loose coupling between services. How does this pattern support the autonomous behavior of self-evolving systems?",
            "Discuss the concept of domain-driven design in the context of intelligent mesh architectures. How do bounded contexts help manage the complexity of large-scale distributed systems?",
        ],
        3: [
            "Compare supervised, unsupervised, and reinforcement learning in the context of enterprise applications. For each paradigm, provide a specific example of how it might be used in a self-evolving system.",
            "Discuss the role of transformer architectures and large language models in enterprise AI. What are the practical considerations for deploying LLMs in a business environment?",
            "How do vector databases and semantic search change the way enterprises manage and retrieve knowledge? Discuss the advantages and limitations compared to traditional relational databases.",
            "Analyze the concept of model drift and its implications for production ML systems. What strategies should self-evolving systems employ to detect and mitigate model drift?",
            "Discuss the importance of MLOps in the context of self-evolving systems. How does automated model lifecycle management differ from traditional software deployment practices?",
        ],
        4: [
            "Explain the concept of the cognitive tax and its impact on resource management in AI-driven systems. How should organizations budget for the computational costs of autonomous decision-making?",
            "Discuss the role of token economics in managing large language model deployments. How can organizations optimize their token usage without sacrificing the quality of AI outputs?",
            "Analyze the concept of hierarchical model orchestration. How does routing different tasks to appropriately sized models improve both cost efficiency and performance?",
            "Discuss the environmental implications of large-scale AI systems. What role does Green AI play in the responsible development of self-evolving enterprise platforms?",
            "How does edge computing change the resource management equation for enterprise AI? Discuss the unique challenges of managing AI workloads at the edge versus the cloud.",
        ],
        5: [
            "Compare the circuit breaker and bulkhead resilience patterns. In what scenarios would you choose one over the other, and how do they complement each other in a comprehensive resilience strategy?",
            "Discuss the philosophy of anti-fragile system design. How does anti-fragility go beyond mere resilience, and what architectural patterns support it in self-evolving systems?",
            "Analyze the role of chaos engineering in building resilient self-evolving systems. What are the risks of chaos engineering, and how can organizations implement it safely?",
            "How do distributed consensus algorithms support the autonomous operation of self-evolving systems? Discuss the trade-offs between consistency and availability in the context of the CAP theorem.",
            "Discuss the concept of graceful degradation in self-evolving systems. How can AI help determine which capabilities to sacrifice when the system is under stress?",
        ],
        6: [
            "Analyze the potential and limitations of AI-generated code. What level of human review is necessary for code produced by generative AI, and how might this change over time?",
            "Discuss the concept of model-driven architecture enhanced by generative AI. How does the combination of traditional MDA practices with LLMs change the software development process?",
            "How might AI-assisted schema design change the role of database administrators? Discuss both the benefits and risks of automating database design decisions.",
            "Analyze the role of AI in automated test generation. Can AI-generated tests achieve the same level of coverage and effectiveness as tests written by experienced QA engineers?",
            "Discuss the ethical and legal implications of AI-generated code. Who is responsible when AI-generated code causes a system failure, and how should organizations manage this liability?",
        ],
        7: [
            "Compare the data fabric and data mesh paradigms. Under what organizational and technical conditions would you recommend one approach over the other?",
            "Discuss the role of data quality in the context of self-evolving systems. How does poor data quality affect the ability of AI systems to make reliable autonomous decisions?",
            "Analyze the importance of data lineage in an AI-driven enterprise. How does understanding data provenance support both operational excellence and regulatory compliance?",
            "Discuss the challenges of implementing real-time data streaming in a large enterprise. What architectural patterns and technologies are most effective for managing high-velocity data flows?",
            "How do knowledge graphs enhance the capabilities of self-evolving systems? Discuss specific use cases where knowledge graphs provide advantages over traditional relational or document databases.",
        ],
        8: [
            "Explain the exploration-exploitation trade-off in the context of enterprise reinforcement learning. How should a self-evolving system balance the need to try new strategies with the need to exploit known-good configurations?",
            "Discuss the challenges of designing effective reward functions for enterprise RL systems. How can organizations ensure that reward functions align with long-term business objectives rather than short-term metrics?",
            "Analyze the concept of multi-agent reinforcement learning in enterprise environments. How do multiple RL agents coordinate their actions to optimize system-wide performance?",
            "Discuss the safety considerations of applying reinforcement learning to production systems. What guardrails are necessary to prevent RL agents from making harmful decisions?",
            "How does reinforcement learning differ from traditional optimization techniques for enterprise resource management? In what scenarios does RL offer clear advantages?",
        ],
        9: [
            "Discuss the evolution of the security perimeter in the age of self-evolving systems. How does the concept of a perimeter change when systems are distributed across clouds, edges, and on-premise environments?",
            "Analyze the role of AI in threat detection and response. How do AI-powered security tools compare to traditional signature-based approaches, and what are their limitations?",
            "Discuss the challenges of implementing zero trust architecture in a large enterprise. What are the organizational and technical barriers, and how can they be overcome?",
            "How should organizations approach the security of their AI models themselves? Discuss threats such as model poisoning, adversarial attacks, and model extraction.",
            "Analyze the role of automated incident response in self-evolving systems. What decisions can be safely automated, and which should always require human approval?",
        ],
        10: [
            "Discuss the importance of explainability in enterprise AI systems. How does the need for explainability vary across different use cases, such as healthcare, finance, and operations management?",
            "Compare the LIME and SHAP explainability methods. What are the strengths and weaknesses of each, and in what scenarios would you choose one over the other?",
            "Analyze the concept of deep observability for AI systems. How does observing an AI system differ from observing a traditional software application, and what additional tools and techniques are needed?",
            "Discuss the role of audit trails in AI governance. How should organizations design their logging and tracing infrastructure to support both operational debugging and regulatory compliance?",
            "How does the observability of AI models in production contribute to the self-evolution capability of the overall system? Discuss the feedback loop between observability data and model improvement.",
        ],
        11: [
            "Discuss the challenges of scaling AI workloads compared to traditional web applications. What unique considerations arise from the computational demands of AI inference and training?",
            "Analyze the concept of AI-driven auto-scaling. How do predictive scaling approaches improve upon reactive scaling, and what data does the system need to make accurate scaling predictions?",
            "Discuss the implications of multi-cloud and hybrid cloud strategies for self-evolving systems. How do organizations manage consistency and interoperability across different cloud providers?",
            "How does database scaling (sharding, replication) change in the context of self-evolving systems? Discuss the role of AI in automating database scaling decisions.",
            "Analyze the cost-performance trade-offs in scaling self-evolving systems. How can organizations optimize their infrastructure spending while maintaining the performance required for autonomous operations?",
        ],
        12: [
            "Discuss the evolution from traditional IT operations to AIOps. What fundamental changes in tooling, processes, and culture are required for successful AIOps adoption?",
            "Analyze the role of AI in root cause analysis. How do AI-driven approaches compare to traditional runbook-based troubleshooting, and what are the limitations of automated root cause analysis?",
            "Discuss the concept of AI-enhanced CI/CD pipelines. How can AI improve the speed and reliability of the software delivery process while maintaining quality standards?",
            "How does the concept of service level objectives (SLOs) change in the context of AIOps? Discuss how AI can help set, monitor, and achieve SLOs more effectively.",
            "Analyze the potential impact of fully autonomous software lifecycle management. What are the risks and benefits of removing human operators from the deployment and operations pipeline?",
        ],
        13: [
            "Discuss the ethical frameworks that should guide the development of self-evolving systems. How do existing frameworks such as IEEE Ethically Aligned Design and EU AI Act apply to autonomous enterprise platforms?",
            "Analyze the concept of bias in AI-driven enterprise decisions. How can organizations detect and mitigate bias in self-evolving systems, and what role should human oversight play?",
            "Discuss the balance between automation and human agency in self-evolving systems. Where should the line be drawn between autonomous decision-making and human control?",
            "How should organizations structure their AI governance bodies? Discuss the roles, responsibilities, and authority of AI ethics committees, model review boards, and responsible AI teams.",
            "Analyze the privacy implications of self-evolving systems that continuously collect and analyze operational data. How can organizations comply with regulations like GDPR and CCPA while maintaining the data flows needed for self-evolution?",
        ],
        14: [
            "Based on the case studies presented, identify the common success factors and pitfalls in implementing self-evolving systems. What patterns emerge across different industries and organizational sizes?",
            "Discuss the change management challenges of transitioning to self-evolving systems. How can organizations overcome resistance to change and build the organizational capabilities needed for success?",
            "Analyze the ROI considerations for self-evolving system implementations. How should organizations measure the return on investment when the benefits are often intangible, such as improved agility and reduced risk?",
            "Discuss the role of pilot programs in self-evolving system adoption. How should organizations design and evaluate pilot programs to maximize learning and minimize risk?",
            "What lessons from the case studies are most applicable to your own organization? Identify specific opportunities where self-evolving system principles could be applied to improve operations.",
        ],
        15: [
            "Discuss the potential impact of quantum computing on enterprise AI. What types of optimization problems in self-evolving systems might benefit most from quantum advantage?",
            "Analyze the concept of neuromorphic computing for edge AI applications. How might neuromorphic chips change the capabilities of self-evolving systems at the edge?",
            "Discuss the path from narrow AI to artificial general intelligence. What implications would AGI have for enterprise architecture, and how should organizations prepare?",
            "How will the concept of the self-evolving enterprise change over the next decade? Discuss your predictions for the future of autonomous enterprise platforms.",
            "Reflect on the human role in an increasingly autonomous enterprise. How can organizations ensure that technology remains a tool for human empowerment rather than a replacement for human judgment?",
        ],
    }

    for ch_num, ch_title in enumerate(chapter_titles, 1):
        add_subheading(doc, "Chapter %d: %s" % (ch_num, ch_title))
        questions = discussion_questions.get(ch_num, [])
        for qi, question in enumerate(questions, 1):
            add_formatted_paragraph(doc, "%d. %s" % (qi, question), first_line_indent=False,
                                    space_after=Pt(8))

    # ========================================
    # APPENDIX B: Technology Reference Guide
    # ========================================
    print("Adding Appendix B: Technology Reference Guide...")
    add_page_break(doc)
    add_heading1(doc, "Appendix B: Technology Reference Guide")

    add_subheading(doc, "B.1 Cloud Platforms and Services")
    add_formatted_paragraph(doc, "The selection of cloud platform is a critical decision in any self-evolving system implementation. Each major cloud provider offers a comprehensive suite of AI and ML services, container orchestration, serverless computing, and data analytics tools. Amazon Web Services (AWS), Microsoft Azure, and Google Cloud Platform (GCP) are the three dominant providers, each with its own strengths and ecosystem advantages. AWS offers the broadest range of services and the largest market share, making it a default choice for many enterprises. Azure integrates deeply with the Microsoft ecosystem, making it attractive for organizations with existing investments in Microsoft technologies. GCP excels in AI and data analytics, offering services like BigQuery, Vertex AI, and TensorFlow Enterprise that are particularly well-suited for self-evolving system architectures.")
    add_formatted_paragraph(doc, "Organizations should consider factors such as existing technology investments, team expertise, geographic availability, pricing models, and the specific AI and ML capabilities offered by each platform. Multi-cloud strategies are increasingly common, allowing organizations to leverage the strengths of multiple providers while avoiding vendor lock-in. However, multi-cloud architectures add complexity to operations and governance, requiring careful planning and the use of abstraction layers to manage interoperability.")

    add_subheading(doc, "B.2 Container and Orchestration Technologies")
    add_formatted_paragraph(doc, "Container technologies and their orchestration platforms form the backbone of modern self-evolving architectures. Docker remains the dominant container runtime, providing a standardized way to package and distribute applications with all their dependencies. Kubernetes has emerged as the de facto standard for container orchestration, offering sophisticated capabilities for deployment, scaling, networking, and self-healing of containerized workloads. Major cloud providers offer managed Kubernetes services (EKS on AWS, AKS on Azure, GKE on GCP) that reduce the operational burden of managing Kubernetes clusters.")
    add_formatted_paragraph(doc, "Beyond basic container orchestration, service mesh technologies such as Istio, Linkerd, and Consul provide advanced networking capabilities including traffic management, security, and observability at the service-to-service communication level. These technologies are essential for implementing the intelligent mesh architectures discussed in this book, as they provide the infrastructure for AI-driven traffic routing, canary deployments, and zero-trust security.")

    add_subheading(doc, "B.3 Machine Learning and AI Frameworks")
    add_formatted_paragraph(doc, "The landscape of machine learning and AI frameworks continues to evolve rapidly. TensorFlow and PyTorch remain the two dominant deep learning frameworks, with PyTorch gaining significant momentum in the research community and TensorFlow maintaining its strength in production deployment scenarios. For traditional machine learning tasks, scikit-learn provides a comprehensive library of algorithms with a consistent and well-designed API. Apache Spark MLlib offers distributed machine learning capabilities for large-scale data processing.")
    add_formatted_paragraph(doc, "The Hugging Face ecosystem has become the central hub for natural language processing, providing access to thousands of pre-trained models and a unified API for working with transformers. For reinforcement learning, libraries such as Stable Baselines3, RLlib (part of Ray), and OpenAI Gym provide the tools needed to develop and train RL agents for enterprise optimization tasks. MLflow and Kubeflow offer comprehensive MLOps platforms for managing the end-to-end machine learning lifecycle.")

    add_subheading(doc, "B.4 Observability and Monitoring Tools")
    add_formatted_paragraph(doc, "Effective observability is the foundation of any self-evolving system. The modern observability stack consists of three pillars: metrics, logs, and traces. Prometheus has become the standard for metrics collection and alerting, with Grafana providing visualization and dashboard capabilities. For log management, the ELK Stack (Elasticsearch, Logstash, Kibana) and alternatives like Loki and Splunk offer powerful search and analysis capabilities. Distributed tracing systems such as Jaeger and Zipkin enable teams to follow requests as they flow through complex microservice architectures.")
    add_formatted_paragraph(doc, "For self-evolving systems, these traditional observability tools must be augmented with AI-specific monitoring capabilities. Tools for tracking model performance, data drift, and feature importance are essential for maintaining the intelligence of autonomous systems. Platforms such as Evidently AI, WhyLabs, and Arize provide specialized monitoring for ML models in production, enabling automated detection of model degradation and triggering retraining pipelines when necessary.")

    add_subheading(doc, "B.5 Data Processing and Analytics")
    add_formatted_paragraph(doc, "Data processing infrastructure is critical for self-evolving systems that depend on continuous data flows for learning and adaptation. Apache Kafka has become the standard for event streaming, providing a durable, scalable, and fault-tolerant messaging system for real-time data pipelines. Apache Flink and Apache Spark Streaming offer powerful stream processing capabilities for transforming and analyzing data in real time. For batch processing, Apache Spark remains the dominant framework, offering a unified engine for SQL, streaming, machine learning, and graph processing.")
    add_formatted_paragraph(doc, "Modern data warehouses and lakes, including Google BigQuery, Amazon Redshift, Snowflake, and Databricks, provide the storage and analytics capabilities needed for large-scale data analysis. These platforms increasingly offer built-in machine learning capabilities, allowing organizations to run AI models directly on their data without the need for complex data movement pipelines. The concept of the lakehouse architecture, which combines the flexibility of data lakes with the performance and governance of data warehouses, is gaining traction as a foundation for self-evolving data infrastructure.")

    add_subheading(doc, "B.6 Security and Identity Tools")
    add_formatted_paragraph(doc, "Security tools for self-evolving systems must go beyond traditional firewalls and intrusion detection systems. Zero trust architecture requires continuous verification of identity and authorization, supported by tools such as Okta, Auth0, and cloud-native identity services. Security Information and Event Management (SIEM) platforms like Splunk, Microsoft Sentinel, and Google Chronicle aggregate and analyze security data from across the enterprise. Security Orchestration, Automation, and Response (SOAR) platforms enable automated incident response, a critical capability for self-evolving security architectures.")
    add_formatted_paragraph(doc, "For AI-specific security, tools for model vulnerability scanning, adversarial robustness testing, and privacy-preserving machine learning are essential. Open-source frameworks such as Microsoft Counterfit, IBM ART (Adversarial Robustness Toolbox), and Google Differential Privacy provide capabilities for testing and hardening AI models against adversarial attacks and privacy violations.")

    # ========================================
    # APPENDIX C: Self-Evolving System Assessment Checklist
    # ========================================
    print("Adding Appendix C: Assessment Checklist...")
    add_page_break(doc)
    add_heading1(doc, "Appendix C: Self-Evolving System Readiness Assessment")

    add_formatted_paragraph(doc, "This appendix provides a comprehensive checklist for organizations evaluating their readiness to implement self-evolving system architectures. The assessment covers five key dimensions: technology infrastructure, data maturity, organizational culture, governance and compliance, and team capabilities. Each dimension includes a set of criteria that should be evaluated on a scale from 1 (not ready) to 5 (fully ready).")

    dimensions = [
        ("C.1 Technology Infrastructure Readiness", [
            "Cloud-native architecture with containerized workloads and orchestration",
            "Microservices or modular architecture with well-defined service boundaries",
            "Service mesh or equivalent infrastructure for service-to-service communication",
            "CI/CD pipelines with automated testing and deployment capabilities",
            "Comprehensive observability stack with metrics, logs, and traces",
            "Event-driven messaging infrastructure for real-time data flows",
            "API-first design with well-documented and versioned interfaces",
            "Infrastructure as Code (IaC) for automated environment provisioning",
            "Disaster recovery and business continuity plans with automated failover",
            "Security infrastructure including identity management and encryption",
        ]),
        ("C.2 Data Maturity Assessment", [
            "Centralized data catalog with metadata management across the organization",
            "Automated data quality monitoring and validation pipelines",
            "Data governance policies with clear ownership and access controls",
            "Real-time data streaming capabilities alongside batch processing",
            "Data lineage tracking for compliance and impact analysis",
            "Feature store or equivalent for ML feature management and reuse",
            "Data privacy controls compliant with relevant regulations (GDPR, CCPA)",
            "Sufficient volume and variety of data for AI model training",
            "Data versioning and reproducibility for model training datasets",
            "Master data management for consistent entity definitions across systems",
        ]),
        ("C.3 Organizational Culture", [
            "Leadership commitment to AI-driven transformation with clear vision",
            "Cross-functional collaboration between business and technology teams",
            "Culture of experimentation with tolerance for controlled failures",
            "Agile or DevOps practices embedded in development and operations",
            "Continuous learning programs for AI, ML, and cloud technologies",
            "Change management processes for technology-driven organizational changes",
            "Innovation incentives and recognition for AI-driven improvements",
            "Open communication channels between teams and leadership",
            "Willingness to restructure roles and responsibilities for autonomous operations",
            "Understanding of AI capabilities and limitations at all organizational levels",
        ]),
        ("C.4 Governance and Compliance", [
            "AI ethics framework with clear principles and guidelines",
            "Model governance processes including review boards and approval workflows",
            "Audit and compliance mechanisms for AI-driven decisions",
            "Privacy impact assessments for data used in AI systems",
            "Explainability requirements defined for high-stakes AI decisions",
            "Incident response procedures for AI-related failures and issues",
            "Regulatory mapping for AI regulations in relevant jurisdictions",
            "Third-party AI model and service risk assessment procedures",
            "Documentation standards for AI models, data, and decisions",
            "Regular governance reviews and updates to AI policies",
        ]),
        ("C.5 Team Capabilities", [
            "Data engineering skills for building and maintaining data pipelines",
            "Machine learning engineering expertise for model development and deployment",
            "MLOps capabilities for automated model lifecycle management",
            "Cloud architecture expertise with certification on major cloud platforms",
            "Security expertise including AI-specific security considerations",
            "DevOps and SRE skills for managing distributed systems",
            "Domain expertise to guide AI application in business contexts",
            "Product management skills for AI-powered product development",
            "Research capabilities for evaluating and adopting emerging AI technologies",
            "Leadership skills for managing AI-driven organizational change",
        ]),
    ]

    for dim_title, items in dimensions:
        add_subheading(doc, dim_title)
        for item in items:
            add_bullet_point(doc, item)

    # ========================================
    # Update footers for all sections
    # ========================================
    print("Updating footers...")
    for section in doc.sections:
        setup_page_layout(section)
        add_footer(section, BOOK_TITLE)

    # Save
    print("Saving expanded document...")
    doc.save("sample_manuscript.docx")

    # Stats
    total_words = sum(len(p.text.split()) for p in doc.paragraphs if p.text.strip())
    estimated_pages = total_words // 250
    print("\n=== EXPANDED DOCUMENT STATISTICS ===")
    print("Total paragraphs: %d" % len(doc.paragraphs))
    print("Total words: %d" % total_words)
    print("Estimated pages: %d" % estimated_pages)
    print("Tables: %d" % len(doc.tables))
    print("\nDocument saved successfully!")


if __name__ == "__main__":
    main()
