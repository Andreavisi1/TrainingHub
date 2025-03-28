import os
import json
import argparse
from typing import Dict, List, Any
import PyPDF2
import docx
from llama_cpp import Llama

class CVSkillsExtractor:
    def __init__(self, model_path: str):
        """
        Inizializza l'estrattore di competenze con il modello Llama specificato.
        
        Args:
            model_path: Percorso al file del modello Llama
        """
        self.model = Llama(
            model_path=model_path,
            n_ctx=2048,          # Contesto massimo
            n_batch=512,         # Dimensione del batch
            n_gpu_layers=-1      # Usa tutte le layer GPU disponibili
        )
        
    def extract_text_from_pdf(self, file_path: str) -> str:
        """Estrae testo da un file PDF."""
        text = ""
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text
    
    def extract_text_from_docx(self, file_path: str) -> str:
        """Estrae testo da un file DOCX."""
        doc = docx.Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    
    def extract_text(self, file_path: str) -> str:
        """Estrae testo dal documento in base all'estensione."""
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        
        if ext == '.pdf':
            return self.extract_text_from_pdf(file_path)
        elif ext == '.docx':
            return self.extract_text_from_docx(file_path)
        elif ext == '.txt':
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        else:
            raise ValueError(f"Formato file non supportato: {ext}")
    
    def extract_skills(self, cv_text: str) -> Dict[str, Any]:
        """
        Estrae le competenze dal testo del CV usando il modello Llama.
        
        Args:
            cv_text: Testo del curriculum
            
        Returns:
            Dizionario con le competenze estratte
        """
        prompt = f"""
        Analizza il seguente curriculum e estrai tutte le competenze tecniche, soft skills, 
        lingue conosciute e certificazioni. Organizza le informazioni in una struttura JSON.
        
        Curriculum:
        {cv_text}
        
        Estrai le seguenti informazioni e formattale in JSON con questa struttura:
        {{
            "technical_skills": ["skill1", "skill2", ...],
            "soft_skills": ["skill1", "skill2", ...],
            "languages": [
                {{"language": "nome lingua", "level": "livello"}},
                ...
            ],
            "certifications": ["cert1", "cert2", ...]
        }}
        
        Output JSON:
        """
        
        # Generiamo il completamento con Llama
        output = self.model(
            prompt,
            max_tokens=2048,
            temperature=0.1,
            top_p=0.9,
            stop=["```"],
            echo=False
        )
        
        # Estraiamo la parte JSON dalla risposta
        response_text = output["choices"][0]["text"]
        
        # Cerchiamo di estrarre solo la parte JSON
        try:
            # Troviamo l'inizio del JSON
            start_idx = response_text.find('{')
            if start_idx == -1:
                raise ValueError("Nessun JSON trovato nella risposta")
            
            # Cerchiamo la fine del JSON
            json_str = response_text[start_idx:]
            
            # Convertiamo il testo in JSON
            skills_dict = json.loads(json_str)
            return skills_dict
        except json.JSONDecodeError:
            # Se c'è un errore nel parsing JSON, ritorniamo un dizionario con la risposta grezza
            return {
                "error": "Errore nel parsing JSON",
                "raw_response": response_text
            }

def main():
    parser = argparse.ArgumentParser(description='Estrai competenze da un CV')
    parser.add_argument('--cv', required=True, help='Percorso al file CV (PDF, DOCX, TXT)')
    parser.add_argument('--model', required=True, help='Percorso al modello Llama')
    parser.add_argument('--output', default='skills.json', help='File di output JSON')
    args = parser.parse_args()
    
    extractor = CVSkillsExtractor(args.model)
    
    try:
        # Estrai il testo dal CV
        cv_text = extractor.extract_text(args.cv)
        
        # Estrai le competenze
        skills = extractor.extract_skills(cv_text)
        
        # Salva il risultato in un file JSON
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(skills, f, ensure_ascii=False, indent=2)
            
        print(f"Competenze estratte e salvate in {args.output}")
        
    except Exception as e:
        print(f"Errore durante l'elaborazione: {str(e)}")

if __name__ == "__main__":
    main()

