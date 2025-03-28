from flask import Flask, request, jsonify, render_template
import os
from werkzeug.utils import secure_filename
from datetime import datetime


app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Sample data for dynamic content
user_data = {
    'name': 'Luca Bellante',
    'level': 12,
    'overall_progress': 65,
    'xp': 2450,
    'badges_count': 8,
    'recent_activities': [
        {
            'icon': 'check-circle',
            'color': 'indigo',
            'message': 'Completato modulo "Comunicazione efficace nel team"',
            'time': '2 ore fa',
            'xp': 150
        },
        {
            'icon': 'award',
            'color': 'green',
            'message': 'Badge ottenuto: "Team Player"',
            'time': 'Ieri',
            'xp': 200
        }
    ],
    'recommended_courses': [
        {
            'title': 'Negoziazione Avanzata',
            'type': 'Soft Skill',
            'duration': '2 ore',
            'modules': 4
        },
        {
            'title': 'Analisi Dati per Decision Making',
            'type': 'Hard Skill',
            'duration': '3 ore',
            'modules': 5
        }
    ],


    'skills': [{
        'leadership': 10,
        'technical': 70,
        'communication': 30,
        'problem_solving': 20,
        'teamwork': 40,
        'creativity': 50}

    ],

    'skills_count': 10
}

skills_data = {
    'hard_skills': [
        {'name': 'Excel', 'level': 85, 'level_text': 'Avanzato'},
        {'name': 'Project Management', 'level': 68, 'level_text': 'Intermedio'},
        {'name': 'Power BI', 'level': 42, 'level_text': 'Base'},
        {'name': 'Metodologie Agile', 'level': 65, 'level_text': 'Intermedio'}
    ],
    'soft_skills': [
        {'name': 'Comunicazione', 'level': 88, 'level_text': 'Avanzato'},
        {'name': 'Problem Solving', 'level': 82, 'level_text': 'Avanzato'},
        {'name': 'Leadership', 'level': 62, 'level_text': 'Intermedio'},
        {'name': 'Lavoro di squadra', 'level': 90, 'level_text': 'Avanzato'}
    ],
    'developing_skills': [
        {
            'name': 'Gestione Conflitti',
            'type': 'Soft Skill',
            'progress': 45
        },
        {
            'name': 'Data Analysis',
            'type': 'Hard Skill',
            'progress': 72
        }
    ]
}


tasks_db = {
    1: {
        'id': 1,
        'title': "Implementazione nuovo modulo analytics",
        'team': "Data Science",
        'deadline': "28/03/2025",
        'days_remaining': 1,
        'status': "In corso",
        'priority': "Alta",
        'assigned_by': "Marco Bianchi",
        'assigned_by_avatar': "user1.jpg",
        'assigned_date': "15/03/2025",
        'user_id': 1,
        'description': "Implementare un nuovo modulo di analytics che permetta di monitorare in tempo reale le performance del sistema e generare report automatici. Il modulo dovrà integrarsi con il database esistente e fornire visualizzazioni interattive dei dati raccolti.",
        'objectives': [
            "Analizzare i requisiti e definire le metriche chiave",
            "Sviluppare query ottimizzate per l'estrazione dei dati",
            "Creare dashboard interattive con filtri personalizzabili",
            "Implementare sistema di report automatici settimanali/mensili",
            "Documentare l'architettura e l'utilizzo del modulo"
        ],
        'required_skills': [
            {"name": "Python", "level": "Advanced"},
            {"name": "SQL", "level": "Advanced"},
            {"name": "Data Visualization", "level": "Intermediate"},
            {"name": "Database Design", "level": "Intermediate"},
            {"name": "ETL", "level": "Beginner"}
        ],
        'collaborators': [

        ]
    },
    2: {
        'id': 2,
        'title': "Ottimizzazione query database",
        'team': "Backend",
        'deadline': "05/04/2025",
        'days_remaining': 9,
        'status': "In corso",
        'priority': "Media",
        'assigned_by': "Giulia Bianchi",
        'assigned_by_avatar': "user5.jpg",
        'assigned_date': "10/03/2025",
        'user_id': 1,
        'description': "Rivedere e ottimizzare le query SQL esistenti per migliorare le performance dell'applicazione. Identificare i colli di bottiglia, creare indici appropriati e rifattorizzare le query più pesanti.",
        'objectives': [
            "Analizzare le performance attuali ed identificare le query critiche",
            "Ottimizzare indici e struttura della base dati",
            "Rifattorizzare le query con particolare attenzione ai join complessi",
            "Implementare caching dove appropriato",
            "Documentare le modifiche e i miglioramenti di performance"
        ],
        'required_skills': [
            {"name": "SQL", "level": "Advanced"},
            {"name": "Database Optimization", "level": "Advanced"},
            {"name": "Performance Tuning", "level": "Intermediate"},
            {"name": "PostgreSQL", "level": "Intermediate"},
            {"name": "Indexing Strategies", "level": "Advanced"}
        ],
        'collaborators': [
            {"name": "Marco Esposito", "avatar": "user6.jpg"},
            {"name": "Anna Ferrari", "avatar": "user7.jpg"}
        ]
    },
    3: {
        'id': 3,
        'title': "Review documentazione API",
        'team': "Documentazione",
        'deadline': "10/04/2025",
        'days_remaining': 14,
        'status': "In attesa",
        'priority': "Bassa",
        'assigned_by': "Paolo Neri",
        'assigned_by_avatar': "user8.jpg",
        'assigned_date': "05/03/2025",
        'user_id': 1,
        'description': "Revisionare la documentazione delle API esistenti, assicurandosi che sia completa, accurata e aggiornata con le ultime modifiche. Aggiungere esempi di utilizzo e migliorare la chiarezza delle spiegazioni.",
        'objectives': [
            "Verificare la completezza della documentazione per tutti gli endpoint",
            "Aggiungere esempi di richieste e risposte per ogni operazione",
            "Migliorare la spiegazione dei parametri e dei possibili errori",
            "Creare guide rapide per i casi d'uso più comuni",
            "Assicurarsi che la documentazione segua gli standard OpenAPI"
        ],
        'required_skills': [
            {"name": "Technical Writing", "level": "Intermediate"},
            {"name": "REST API", "level": "Intermediate"},
            {"name": "Swagger/OpenAPI", "level": "Beginner"},
            {"name": "Markdown", "level": "Intermediate"},
            {"name": "API Testing", "level": "Beginner"}
        ],
        'collaborators': [
            {"name": "Chiara Romano", "avatar": "user9.jpg"}
        ]
    },
    4: {
        'id': 4,
        'title': "Demo cliente progetto X",
        'team': "Product",
        'deadline': "01/04/2025",
        'days_remaining': 5,
        'status': "Bloccato",
        'priority': "Alta",
        'assigned_by': "Simone Ricci",
        'assigned_by_avatar': "user10.jpg",
        'assigned_date': "20/02/2025",
        'user_id': 1,
        'description': "Preparare e condurre una demo del prodotto per un cliente importante. La presentazione dovrà evidenziare le funzionalità chiave, i benefici rispetto alla concorrenza e rispondere alle domande tecniche e di business.",
        'objectives': [
            "Preparare slide e script per la presentazione",
            "Configurare ambiente demo con dati realistici",
            "Coordinare con il team di vendita per allineare i messaggi chiave",
            "Preparare risposte alle possibili domande tecniche",
            "Condurre la demo e raccogliere feedback"
        ],
        'required_skills': [
            {"name": "Presentation Skills", "level": "Advanced"},
            {"name": "Product Knowledge", "level": "Advanced"},
            {"name": "Communication", "level": "Advanced"},
            {"name": "Demo Preparation", "level": "Intermediate"},
            {"name": "Client Management", "level": "Intermediate"}
        ],
        'collaborators': [
            {"name": "Roberto Marini", "avatar": "user11.jpg"},
            {"name": "Elena Costa", "avatar": "user12.jpg"}
        ]
    }
}

# Mock courses database
courses_db = [
    {
        'id': 1,
        'title': "Advanced Data Structures in Python",
        'platform': "Coursera",
        'platform_logo': "coursera.png",
        'category': "Coding",
        'level': "Advanced",
        'duration': "56 ore",
        'rating': 4.8,
        'priority': "Alta",
        'description': "Approfondisci la tua conoscenza delle strutture dati e degli algoritmi con questo corso avanzato di Stanford University.",
        'skills': ["Data cleaning", "Data transformation", "Performance optimization"],
        'task_ids': [1, 2],
        'topic': "python.png"
    },
    {
        'id': 2,
        'title': "Front-End Mastery: dai pixel al codice",
        'platform': "LinkedIn Learning",
        'platform_logo': "linkedin.png",
        'category': "Team",
        'level': "Intermediate",
        'duration': "28 ore",
        'rating': 4.2,
        'priority': "Media",
        'description': "Dall'HTML5 alle animazioni, Javascript e React, costruirai progetti reali e svilupperai le competenze per distinguerti nel mondo del web.",
        'skills': ["Frontend", "HTML", "Javascript", "React"],
        'task_ids': [4],
        'topic': "html.jpg"

    },
    {
        'id': 3,
        'title': "Critical Thinking & Problem Solving Mastery",
        'platform': "Udemy",
        'platform_logo': "udemy.png",
        'category': "Problem Solving",
        'level': "Beginner",
        'duration': "18 ore",
        'rating': 4.9,
        'priority': "Bassa",
        'description': "Sviluppa tecniche avanzate di pensiero critico e risoluzione dei problemi, applicabili in ambito lavorativo e personale.",
        'skills': ["Critical Thinking", "Problem Analysis", "Decision Making"],
        'task_ids': [1, 3, 4],
        'topic': "critical_thinking.png"

    },
    {
        'id': 4,
        'title': "Data Analysis con Python: Pandas Avanzato",
        'platform': "DataCamp",
        'platform_logo': "datacamp.png",
        'category': "Data Science",
        'level': "Advanced",
        'duration': "12 ore",
        'rating': 4.8,
        'priority': "Alta",
        'description': "Questo corso approfondisce l'uso di Pandas per l'analisi dei dati e la manipolazione di dataset complessi. Imparerai tecniche di aggregazione, pulizia dati e trasformazione che sono essenziali per il tuo task corrente.",
        'skills': ["Data cleaning", "Data transformation", "Performance optimization"],
        'task_ids': [1],
        'topic': "python"
    },
    {
        'id': 5,
        'title': "Data Visualization con Matplotlib e Seaborn",
        'platform': "Coursera",
        'platform_logo': "coursera.png",
        'category': "Data Science",
        'level': "Intermediate",
        'duration': "18 ore",
        'rating': 4.1,
        'priority': "Media",
        'description': "Impara a creare visualizzazioni efficaci e interattive dai tuoi dati. Questo corso copre le librerie principali di Python per la visualizzazione e ti aiuterà a presentare i risultati delle tue analisi in modo professionale.",
        'skills': ["Data storytelling", "Visualizzazione statistica", "Interactive dashboards"],
        'task_ids': [1],
        'topic': "python"

    },
    {
        'id': 6,
        'title': "Ottimizzazione delle Query SQL per Big Data",
        'platform': "Udemy",
        'platform_logo': "udemy.png",
        'category': "Database",
        'level': "Advanced",
        'duration': "15 ore",
        'rating': 4.9,
        'priority': "Media",
        'description': "Questo corso ti insegnerà le tecniche più avanzate per ottimizzare le query SQL quando lavori con grandi volumi di dati, migliorando le performance delle tue analisi.",
        'skills': ["Query optimization", "Index management", "Performance tuning"],
        'task_ids': [1, 2],
        'topic': "python"

    },
    {
        'id': 7,
        'title': "Machine Learning per Data Analytics",
        'platform': "edX",
        'platform_logo': "edx.png",
        'category': "Data Science",
        'level': "Intermediate",
        'duration': "24 ore",
        'rating': 4.0,
        'priority': "Bassa",
        'description': "Un'introduzione ai concetti di machine learning applicati all'analisi dei dati. Questo corso ti darà una comprensione di come implementare modelli semplici per analisi predittive e classificazione.",
        'skills': ["Regression", "Classification", "Feature engineering"],
        'task_ids': [1],
        'topic': "python"

    }
]

# Additional resources for tasks
resources_db = [
    {
        'id': 1,
        'title': "Python for Data Science Handbook",
        'platform': "O'Reilly",
        'duration': "Libro (546 pagine)",
        'rating': 4.9,
        'priority': "Media",
        'task_ids': [1]
    },
    {
        'id': 2,
        'title': "SQL Performance Explained",
        'platform': "Modern SQL",
        'duration': "Ebook (204 pagine)",
        'rating': 4.6,
        'priority': "Media",
        'task_ids': [2]
    },
    {
        'id': 3,
        'title': "Database Systems: The Complete Book",
        'platform': "Pearson",
        'duration': "Libro (1119 pagine)",
        'rating': 4.2,
        'priority': "Bassa",
        'task_ids': [2]
    }
]

@app.route('/')
def dashboard():
    # Get user tasks
    user_tasks = [task for task_id, task in tasks_db.items()]
    
    # Get recommended courses based on user skills
    recommended_courses = []
    for course in courses_db:
        if len(recommended_courses) < 3:  # Limit to 3 courses for now
            recommended_courses.append(course)
    
    return render_template('dashboard.html', 
                          user=user_data, 
                          user_tasks=user_tasks,
                          recommended_courses=recommended_courses)

@app.route('/onboarding')
def onboarding():
    return render_template('onboardingPage.html', 
                           user=user_data)

@app.route('/learning')
def learning():
    return render_template('learning.html',
                           user=user_data)

@app.route('/skills')
def skills():
    return render_template('manager-dashboard.html', 
                           user=user_data,
                           skills=skills_data)

@app.route('/task/<int:task_id>')
def task_detail(task_id):
    task = tasks_db.get(task_id)
    
    
    # Get recommended courses for this task
    task_courses = [course for course in courses_db if task_id in course['task_ids']]
    # Sort by priority
    task_courses.sort(key=lambda x: {'Alta': 0, 'Media': 1, 'Bassa': 2}[x['priority']])
    
    # Get additional resources
    task_resources = [resource for resource in resources_db if task_id in resource['task_ids']]
    
    return render_template('task_detail.html', 
                          user=user_data,
                          task=task,
                          courses=task_courses,
                          resources=task_resources)

@app.route('/all_courses')
def allCourses():
    return render_template('allCourses.html',
                           user=user_data)

@app.route('/upload-files', methods=['POST'])
def upload_files():
    # Crea una sottocartella con timestamp per ogni upload
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    upload_subfolder = os.path.join(app.config['UPLOAD_FOLDER'], f"upload_{timestamp}")
    os.makedirs(upload_subfolder)
    
    files_saved = 0
    
    if 'files' not in request.files:
        return jsonify({'error': 'Nessun file inviato'}), 400
    
    files = request.files.getlist('files')
    
    for file in files:
        if file.filename == '':
            continue
            
        # Sanitizza il nome del file per sicurezza
        filename = secure_filename(file.filename)
        file_path = os.path.join(upload_subfolder, filename)
        
        # Salva il file
        file.save(file_path)
        files_saved += 1
    
    return jsonify({
        'success': True,
        'message': f'{files_saved} file salvati con successo',
        'folderPath': upload_subfolder
    })


if __name__ == '__main__':
    app.run(debug=True)