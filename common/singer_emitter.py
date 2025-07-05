import singer

#Classe generica para os metodos do singer

class SingerEmitter:
    """
    Classe genérica para emitir mensagens Singer.
    Pode ser usada em qualquer Tap.
    """

    def write_schema(self, stream_name: str, schema: dict, key_properties: list):
        """
        Emite o SCHEMA da stream.

        :param stream_name: Nome da stream
        :param schema: JSON Schema (dict)
        :param key_properties: Lista de campos que são PKs ou campos únicos
        """
        singer.write_schema(stream_name, schema, key_properties)
    
    def write_state(self, state: dict):
        """
        Emite estado para salvar progresso de execução.
        """
        singer.write_state(state)
    
    def write_record(self, stream_name: str, record: dict):
        """
        Emite um registro da stream.
        """
        singer.write_record(stream_name, record)

    def write_batch_records(self, stream_name: str, records: list):
        """
        Emite vários registros de uma vez.
        """
        for record in records:
            self.write_record(stream_name, record)
