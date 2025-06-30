import pickle

save_keys = ['_server_exp_mult', '_server_money_mult', '_server_tax', '_blocked_channels', '_level_up_channel']

class Server:
    id: int
    data_server: dict
    
    _server_exp_mult: float = 1.0 
    _server_money_mult: float = 1.0
    _server_tax: float = 0.0
    _blocked_channels: list = []
    _level_up_channel: int = None
    _buffs: dict = {}
    
    @property
    def server_exp_mult(self): return self._server_exp_mult
    
    @property
    def server_money_mult(self): return self._server_money_mult
    
    @property
    def server_tax(self): return self._server_tax
    
    @property
    def blocked_channels(self): return self._blocked_channels
    @property
    def level_up_channel(self): return self._level_up_channel
    
    @property
    def buffs(self): return self._buffs
    
    @server_exp_mult.setter
    def server_exp_mult(self, value): self._server_exp_mult = value
    @server_money_mult.setter
    def server_money_mult(self, value): self._server_money_mult = value
    @server_tax.setter
    def server_tax(self, value): self._server_tax = value
    @blocked_channels.setter
    def blocked_channels(self, value): self._blocked_channels = value
    @level_up_channel.setter
    def level_up_channel(self, value): self._level_up_channel = value
    @buffs.setter
    def buffs(self, value): self._buffs = value
    
    def __init__(self, id:int):
        self.id = id
        self.data_server = {
            'server_exp_mult': 1.0,
            'server_money_mult': 1.0,
            'server_tax': 0.0,
            'blocked_channels': [],
            'level_up_channel': None,
            'buffs': {}
        }
        
        self.load_data_server()
        
    def load_data_server(self):
        for key in self.data_server.keys():
            self.__dict__[f'_{key}']= self.data_server[key]

    def load(self, data: bytes):
        d:dict = {}
        d = dict(pickle.loads(data))
        s = Server(self.id)
        
        for key in d.keys():
            s.data_server[key] = d[key]
        
        s.load_data_server()
        
        return s
                
    def save(self) -> bytes:
        d = {}
        for key in save_keys:
            if key in self.__dict__.keys():
                d[(key if not key.startswith('_') else key[1:])] = self.__dict__[key]
        return pickle.dumps(d)