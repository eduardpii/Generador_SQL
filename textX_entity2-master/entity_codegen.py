"""
An example how to generate angularjs code from textX model using jinja2
template engine (http://jinja.pocoo.org/docs/dev/)
"""
from os import mkdir
from os.path import exists, dirname, join
import jinja2
from entity_test import get_entity_mm


def main(debug=False):

    this_folder = dirname('__file__')

    entity_mm = get_entity_mm(debug)

    # Build Person model from person.ent file
    person_model = entity_mm.model_from_file(join(this_folder, 'PROGRAMACION.ent'))

    def is_entity(n):
        """
        Test to prove if some type is an entity
        """
        if n.type in person_model.entities:
            return True
        else:
            return False


    # Create output folder
    srcgen_folder = join(this_folder, 'srcgen')
    if not exists(srcgen_folder):
        mkdir(srcgen_folder)

    # Initialize template engine.
    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(this_folder),
        trim_blocks=True,
        lstrip_blocks=True)

    # Register filter for mapping Entity type names to Java type names.

    jinja_env.tests['entity'] = is_entity

    # Load template
    template0 = jinja_env.get_template('sql.template')
    template1 = jinja_env.get_template('ESTADIO.template')
    template2 = jinja_env.get_template('GRUPO.template')
    template3 = jinja_env.get_template('EQUIPO.template')
    
    for entity in person_model.entities:
        # For each entity generate java file
        if entity.name == 'PROGRAMACION':
            with open(join(srcgen_folder,
                       "%s.sql" % entity.name.capitalize()), 'w') as f:
                f.write(template0.render(entity=entity))
        elif entity.name == 'ESTADIO':
            with open(join(srcgen_folder,
                       "%s.sql" % entity.name.capitalize()), 'w') as f:
                f.write(template1.render(entity=entity))
        elif entity.name == 'GRUPO':
            with open(join(srcgen_folder,
                       "%s.sql" % entity.name.capitalize()), 'w') as f:
                f.write(template2.render(entity=entity))
        else:
            with open(join(srcgen_folder,
                       "%s.sql" % entity.name.capitalize()), 'w') as f:
                f.write(template3.render(entity=entity))
        

            


if __name__ == "__main__":
    main()
