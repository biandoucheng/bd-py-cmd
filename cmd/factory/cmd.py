from dataclasses import dataclass

@dataclass
class CmdMeta:
    number:int
    name:str
    alias:str
    desc:str

    def search(self,vl:str="") -> bool:
        """
        Determine if the search matches

        :param vl: str search word
        """
        if not vl:
            return False

        if vl.isdigit():
            return vl == str(self.number)
        
        return vl in self.name or vl in self.alias or vl in self.desc
    

    def say(self,) -> str:
        """
        Describe information
        """
        return f"""
        {self.name} ----------------------
                    {self.alias}
                    {self.desc}
                    Number: {self.number}
        """
