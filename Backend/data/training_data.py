import random
from typing import List, Tuple

def generate_training_data() -> List[Tuple[str, dict, str]]:
    random.seed(42)
    data = []
    
    # Titles (~100)
    title_templates = [
        "Machine Learning for Natural Language Processing",
        "Advanced Signal Processing Techniques",
        "A Comprehensive Study on Deep Neural Networks",
        "Quantum Computing: A New Era",
        "Data Mining and Knowledge Discovery",
        "Understanding Artificial Intelligence",
        "Computer Vision Applications in Healthcare",
        "Blockchain Technology and Its Uses",
        "Cybersecurity in the Modern World",
        "Internet of Things: Challenges and Opportunities"
    ]
    for _ in range(100):
        t = random.choice(title_templates)
        if random.random() > 0.5:
            t = t.upper()
        data.append((t, {'is_bold': True, 'is_italic': False, 'font_size': 18.0, 'position_ratio': random.uniform(0.0, 0.05)}, 'title'))

    # Authors (~100)
    author_templates = [
        "John Smith, Department of Computer Science",
        "Dr. Jane Doe\nUniversity of Oxford",
        "alice@university.edu",
        "Bob Johnson, Alice Williams",
        "Charlie Brown\nDepartment of Physics, MIT",
        "David Clark (david.clark@example.com)"
    ]
    for _ in range(100):
        a = random.choice(author_templates)
        data.append((a, {'is_bold': False, 'is_italic': False, 'font_size': 12.0, 'position_ratio': random.uniform(0.01, 0.05)}, 'author'))

    # Chapter Headings (~300)
    chapter_templates = [
        "CHAPTER {n}",
        "Chapter {n} Introduction",
        "INTRODUCTION",
        "METHODOLOGY",
        "LITERATURE REVIEW",
        "RESULTS AND DISCUSSION",
        "CONCLUSION",
        "ABSTRACT",
        "ACKNOWLEDGMENTS",
        "APPENDIX",
        "BACKGROUND",
        "THEORETICAL FRAMEWORK",
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
        "About the Author",
        "About the Authors",
        "Author Bio"
    ]
    for i in range(300):
        c = random.choice(chapter_templates).replace("{n}", str(random.randint(1, 20)))
        data.append((c, {'is_bold': True, 'is_italic': False, 'font_size': 16.0, 'position_ratio': random.uniform(0.05, 0.9)}, 'chapter_heading'))

    # Section Headings (~400)
    for _ in range(400):
        chap = random.randint(1, 10)
        sec = random.randint(1, 8)
        names = ["Background", "Problem Statement", "Data Collection", "Performance Analysis", "Method", "Results"]
        c = f"{chap}.{sec} {random.choice(names)}"
        data.append((c, {'is_bold': True, 'is_italic': False, 'font_size': 14.0, 'position_ratio': random.uniform(0.1, 0.9)}, 'section_heading'))

    # Subsection Headings (~300)
    for _ in range(300):
        chap = random.randint(1, 10)
        sec = random.randint(1, 8)
        subsec = random.randint(1, 5)
        names = ["Overview", "Feature Extraction", "Results Summary", "Discussion", "Analysis"]
        c = f"{chap}.{sec}.{subsec} {random.choice(names)}"
        data.append((c, {'is_bold': True, 'is_italic': False, 'font_size': 12.0, 'position_ratio': random.uniform(0.1, 0.9)}, 'subsection_heading'))

    # Body Paragraphs (~2000)
    sentences = [
        "The proposed methodology significantly improves the baseline performance.",
        "Data was collected from various sources and preprocessed to remove anomalies.",
        "Figure 1 illustrates the overall architecture of the system.",
        "Our experiments demonstrated a 20% increase in accuracy over previous models.",
        "The algorithm relies on deep neural networks to extract meaningful features.",
        "A comprehensive literature review highlights the gap in existing research.",
        "In this study, we present a novel approach to tackle this problem.",
        "The dataset comprises over ten thousand annotated images.",
        "Parameters were tuned using a grid search over the validation set.",
        "The results suggest that this approach is robust against noise.",
        "Further research is required to fully understand these limitations.",
        "We observed a correlation between variable X and variable Y.",
        "Table 2 summarizes the performance metrics across all datasets.",
        "The computational complexity is O(n log n) in the worst case.",
        "These findings are consistent with the hypothesis proposed earlier."
    ]
    for _ in range(2000):
        num_sentences = random.randint(2, 8)
        para = " ".join(random.choices(sentences, k=num_sentences))
        data.append((para, {'is_bold': False, 'is_italic': False, 'font_size': 12.0, 'position_ratio': random.uniform(0.05, 0.95)}, 'body'))

    # Figure Captions (~300)
    for i in range(300):
        num = random.randint(1, 20)
        sub = random.randint(1, 5)
        temps = [
            f"Figure {num}: System Architecture",
            f"Figure {num}.{sub}: Proposed Framework",
            f"Fig. {num}: Results Comparison",
            f"Figure {num}.{sub}: Performance graph of the proposed method"
        ]
        c = random.choice(temps)
        data.append((c, {'is_bold': False, 'is_italic': True, 'font_size': 10.0, 'position_ratio': random.uniform(0.1, 0.9)}, 'figure_caption'))

    # Table Captions (~300)
    for i in range(300):
        num = random.randint(1, 20)
        sub = random.randint(1, 5)
        temps = [
            f"Table {num}: Experimental Results",
            f"Table {num}.{sub}: Performance Comparison",
            f"Table {num}: Dataset Statistics",
            f"Tbl. {num}: Summary of Parameters"
        ]
        c = random.choice(temps)
        data.append((c, {'is_bold': False, 'is_italic': True, 'font_size': 10.0, 'position_ratio': random.uniform(0.1, 0.9)}, 'table_caption'))

    # Reference Headings (~50)
    ref_heads = ["References", "REFERENCES", "Bibliography", "Works Cited", "Reference", "BIBLIOGRAPHY"]
    for _ in range(50):
        c = random.choice(ref_heads)
        data.append((c, {'is_bold': True, 'is_italic': False, 'font_size': 14.0, 'position_ratio': random.uniform(0.9, 0.98)}, 'reference_heading'))

    # Reference Entries (~500)
    for i in range(500):
        year = random.randint(1990, 2024)
        temps = [
            f"[{i+1}] Smith, J. ({year}). Title of paper. Journal Name, 10(2), 100-115.",
            f"[{i+1}] Doe, A., & Johnson, B. ({year}). Book Title. Publisher.",
            f'Smith, J. et al. "Paper title." Conference Name ({year}): 1-10.',
            f"[{i+1}] A. Einstein and B. Podolsky. Physical Review, {year}."
        ]
        c = random.choice(temps)
        data.append((c, {'is_bold': False, 'is_italic': False, 'font_size': 10.0, 'position_ratio': random.uniform(0.95, 1.0)}, 'reference_entry'))

    # MCQ Headings (~100)
    mcq_h_temps = ["Multiple Choice Questions (MCQs)", "Multiple Choice Questions", "MCQs", "Review Questions", "Chapter Review MCQs"]
    for _ in range(100):
        c = random.choice(mcq_h_temps)
        data.append((c, {'is_bold': True, 'is_italic': False, 'font_size': 12.0, 'position_ratio': random.uniform(0.1, 0.95)}, 'mcq_heading'))

    # MCQ Questions (~400)
    q_starters = [
        "Which of the following best describes the architecture of distributed systems?",
        "Why does adopting zero trust security reduce attack surfaces?",
        "What is the primary role of a cognitive edge gateway?",
        "In modern cloud architectures, how is state managed across microservices?",
        "Which algorithm provides the lowest latency for real-time edge classification?",
        "According to NIST SP 800-207, which tenet is fundamental to Zero Trust?",
        "How do self-evolving platforms handle autonomous failover during node crashes?",
        "What distinguishes fog computing from traditional cloud centralized infrastructure?"
    ]
    for i in range(400):
        q = f"{random.randint(1, 25)}. {random.choice(q_starters)}"
        data.append((q, {'is_bold': True, 'is_italic': False, 'font_size': 12.0, 'position_ratio': random.uniform(0.1, 0.95)}, 'mcq_question'))

    # MCQ Options (~400)
    opt_temps = [
        "a) Increasing monolithic dependencies\nb) Decoupling microservices across edge nodes\nc) Disabling firewall rules\nd) Restricting all network traffic",
        "a) High computational overhead\nb) Dynamic policy enforcement\nc) Manual ticket resolution\nd) Static IP filtering",
        "a) First-in First-out queuing\nb) Priority-based routing\nc) Random load shedding\nd) Round-robin hashing",
        "a) Centralized relational storage\nb) Distributed event-driven ledger\nc) In-memory cache replication\nd) Local disk write-ahead log"
    ]
    for _ in range(400):
        c = random.choice(opt_temps)
        data.append((c, {'is_bold': False, 'is_italic': False, 'font_size': 12.0, 'position_ratio': random.uniform(0.1, 0.95)}, 'mcq_option'))

    # MCQ Answers (~200)
    ans_temps = ["Answer: a)", "Answer: b)", "Answer: c)", "Answer: d)", "Answer: B", "Answer: A - Decoupling microservices"]
    for _ in range(200):
        c = random.choice(ans_temps)
        data.append((c, {'is_bold': True, 'is_italic': False, 'font_size': 12.0, 'position_ratio': random.uniform(0.1, 0.95)}, 'mcq_answer'))

    # Table of Contents / Index Headings (~60)
    toc_heads = ["Table of Contents", "Contents", "INDEX", "Index", "Detailed Index"]
    for _ in range(60):
        c = random.choice(toc_heads)
        data.append((c, {'is_bold': True, 'is_italic': False, 'font_size': 16.0, 'position_ratio': random.uniform(0.01, 0.05)}, 'toc_heading'))

    # Table of Contents / Index Entries (~400)
    for i in range(400):
        c = f"{random.randint(1, 15)}.{random.randint(1, 8)} Topic Name and Overview\t{random.randint(1, 480)}"
        data.append((c, {'is_bold': False, 'is_italic': False, 'font_size': 11.0, 'position_ratio': random.uniform(0.01, 0.08)}, 'toc_entry'))

    # List Items (~300)
    list_temps = [
        "• Item one description",
        "- Second item in the list",
        "* Third bullet point",
        "1. First numbered item",
        "2. Second numbered item",
        "a) Sub item",
        "i. Roman numeral item",
        "▪ Square bullet item"
    ]
    for _ in range(300):
        c = random.choice(list_temps)
        data.append((c, {'is_bold': False, 'is_italic': False, 'font_size': 12.0, 'position_ratio': random.uniform(0.1, 0.9)}, 'list_item'))

    # Blank Entries (~200)
    blanks = ['', '   ', '\n', '\t']
    for _ in range(200):
        c = random.choice(blanks)
        data.append((c, {'is_bold': False, 'is_italic': False, 'font_size': 12.0, 'position_ratio': random.uniform(0.0, 1.0)}, 'blank'))

    return data
