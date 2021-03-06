from EmrData.management.commands.abstractImporter import AbstractImportCommand
from EmrData.OMOPModels.vocabularyModels import DOMAIN


class Command(AbstractImportCommand):
    help = "Import OMOP DOMAIN.csv."

    def printMsg(self):
        print("Importing OMOP Domains...")

    def expectedCsvColumns(self):
        return ['domain_id', 'domain_name', 'domain_concept_id']

    def deleteAllModelInstances(self):
        DOMAIN.objects.all().delete()

    def bulkCreateModelInstances(self, objs):
        DOMAIN.objects.bulk_create(objs)

    @staticmethod
    def makeObjFromRow(row):
        domain_id, domain_name, domain_concept_id = row
        return DOMAIN(domain_id=domain_id, domain_name=domain_name, domain_concept_id=domain_concept_id)

    @staticmethod
    def processRows(rows):
        return [Command.makeObjFromRow(row) for row in rows]

    def asyncProcessData(self, pool, data):
        results = pool.apply_async(Command.processRows, args=(data,))
        return results.get()
