import re
import spacy
from query_templates import SQL_TEMPLATES, identify_intent, identify_table

# Load the spaCy model for NLP
nlp = spacy.load('en_core_web_sm')

class NLPProcessor:
    def __init__(self):
        self.entities = None

    def extract_entities(self, user_input):
        """Extract entities from user input using spaCy."""
        doc = nlp(user_input)
        self.entities = {ent.label_: ent.text for ent in doc.ents}
        return self.entities

    def generate_query_from_entities(self):
        """Generate a SQL query based on extracted entities."""
        if not self.entities:
            return None

        table = identify_table(self.entities.get('ORG', '').lower())
        intent = identify_intent(self.entities.get('MONEY', '').lower())

        if not table or not intent:
            return "Could not generate query. Missing table or intent."

        if intent == 'select':
            columns = self.entities.get('PRODUCT', '*')
            condition = f"{self.entities.get('PERSON', 'name')} = '{self.entities.get('GPE', '')}'"
            query = SQL_TEMPLATES['select'].format(columns=columns, table=table, condition=condition)
            return query

        # Handle other intents similarly (insert, update, delete)
        # ...

        return "Unhandled query generation."

    def refine_query(self, query):
        """Refine a generated SQL query to improve its accuracy."""
        query = query.replace(" WHERE WHERE ", " WHERE ")
        query = query.replace("SELECT *", "SELECT id, name")
        return query

    def handle_query_generation(self, user_input):
        """Process user input and generate an appropriate SQL query."""
        entities = self.extract_entities(user_input)
        query = self.generate_query_from_entities()
        refined_query = self.refine_query(query)
        return refined_query

# Example usage:
if __name__ == "__main__":
    nlp_processor = NLPProcessor()

    # Sample user input
    user_input = "Show me all products ordered by Alice"
    generated_query = nlp_processor.handle_query_generation(user_input)
    print("Generated Query:", generated_query)
