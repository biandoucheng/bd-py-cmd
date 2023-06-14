from dataclasses import dataclass

@dataclass
class MethodMeta:
    number:int
    cname:str
    name:str
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
        
        return vl in self.name or vl in self.desc
    

    def say(self,) -> str:
        """
        Describe information
        """
        return f"""
        *** method check **************
        {self.cname} . {self.name}
                Number: {self.number}
                {self.desc}  
        """


    def info(self,) -> str:
        """
        Describe information
        """
        return f"""
        *** method run ******************
        {self.cname} . {self.name}
        {self.desc}
        """