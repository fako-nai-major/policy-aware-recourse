course_catalog = [
    {
        "course_code": "COMP-200",
        "course_title": "Intro to Java Programming",
        "institution": "AU",
        "recommendation_category": "Computer Science",
        "recommendation_sub_category": "Software Development",
        "overview": (
            "An introductory programming course that uses Java to teach problem "
            "solving, program design, control flow, methods, and foundational "
            "object-oriented concepts."
        ),
        "outcomes": [
            "Explain core programming concepts including variables, expressions, control structures, and methods.",
            "Design and implement small Java programs that solve well-defined problems.",
            "Use classes and objects to model simple real-world entities.",
            "Debug, test, and refine Java programs using systematic development practices.",
        ],
        "objectives": [
            "Write, compile, and run Java applications using standard development tools.",
            "Apply conditional logic, loops, and decomposition to programming tasks.",
            "Create classes with fields, constructors, and methods.",
            "Trace program execution and correct syntax, runtime, and logical errors.",
        ],
        "assignments": {
            "Assignment 1": [
                "articulate the principles of object-oriented problem solving and programming.",
                "outline the essential features and elements of the Java programming language.",
                "explain programming fundamentals, including statement and control flow and recursion.",
            ],
            "Assignment 2": [
                "apply the concepts of class, method, constructor, instance, data abstraction, function abstraction, inheritance, overriding, overloading, and polymorphism.",
                "program with basic data structures using array, list, and linked structures.",
            ],
            "Assignment 3": [
                "explain the object-oriented design process and the concept of software engineering.",
                "program using objects and data abstraction, class, and methods in function abstraction.",
            ],
            "Final project": [
                "analyze, write, debug, and test basic Java codes using the approaches introduced in the course.",
                "analyze problems and implement simple Java applications using an object-oriented software engineering approach.",
            ],
        },
    },
    {
        "course_code": "COMP-254",
        "course_title": "Intro to Data Structures in Java",
        "institution": "AU",
        "recommendation_category": "Computer Science",
        "recommendation_sub_category": "Algorithms",
        "overview": (
            "A second-level programming course focused on implementing and using "
            "fundamental data structures in Java, together with algorithm analysis "
            "and performance trade-offs."
        ),
        "outcomes": [
            "Describe the behavior and applications of common linear and non-linear data structures.",
            "Implement stacks, queues, linked lists, trees, hash tables, and graphs in Java.",
            "Analyze algorithm efficiency using asymptotic notation.",
            "Select suitable data structures based on correctness and performance requirements.",
        ],
        "objectives": [
            "Compare arrays, linked structures, and abstract data types in terms of use cases and complexity.",
            "Implement searching, sorting, traversal, and hashing techniques in Java.",
            "Evaluate algorithmic performance with Big-O time and space analysis.",
            "Test and debug data-structure implementations using representative inputs.",
        ],
        "assignments": {
            "Assignment 1": [
                "implement array-based and linked-list-based collections in Java.",
                "compare the performance of iterative operations on linear data structures.",
            ],
            "Assignment 2": [
                "develop stack and queue abstractions to solve constrained programming problems.",
                "analyze recursive and iterative solutions using asymptotic notation.",
            ],
            "Assignment 3": [
                "construct trees, binary search trees, and hash tables for efficient storage and retrieval.",
                "evaluate collision handling, traversal, and balancing trade-offs.",
            ],
            "Final project": [
                "design and implement a Java solution that integrates multiple data structures.",
                "justify data-structure and algorithm choices using complexity analysis and empirical testing.",
            ],
        },
    },
    {
        "course_code": "COMP-266",
        "course_title": "Intro to Databases",
        "institution": "AU",
        "recommendation_category": "Computer Science",
        "recommendation_sub_category": None,
        "overview": (
            "An introduction to database systems covering relational design, SQL, "
            "normalization, transactions, and practical data modeling for software applications."
        ),
        "outcomes": [
            "Explain core database concepts including schemas, keys, constraints, and relationships.",
            "Design normalized relational databases from application requirements.",
            "Write SQL queries for data definition, manipulation, and retrieval.",
            "Discuss transactions, integrity, security, and database administration basics.",
        ],
        "objectives": [
            "Model entities and relationships using conceptual and logical design techniques.",
            "Create tables, views, and constraints using SQL.",
            "Compose joins, aggregate queries, nested queries, and updates for relational databases.",
            "Assess normalization, indexing, and transaction management choices for data quality and performance.",
        ],
        "assignments": {
            "Assignment 1": [
                "identify entities, relationships, attributes, and keys from a problem description.",
                "construct entity-relationship models for small information systems.",
            ],
            "Assignment 2": [
                "transform conceptual models into relational schemas.",
                "apply first, second, and third normal form to improve schema quality.",
            ],
            "Assignment 3": [
                "write SQL statements for schema creation, querying, insertion, update, and deletion.",
                "use joins and aggregation to answer practical information needs.",
            ],
            "Final project": [
                "design and implement a small database-backed solution for a realistic case study.",
                "justify schema, query, and integrity decisions with reference to usability, consistency, and performance.",
            ],
        },
    },
]


course_data = course_catalog[0]
