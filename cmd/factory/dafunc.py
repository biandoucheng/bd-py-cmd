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
        [ {self.name} ] of {self.cname} . Method Info 
        Number: {self.number}
        {self.desc}  
        """.lstrip("\n")


    def info(self,) -> str:
        """
        Describe information
        """
        return f"""
        >>> Running Son Method : 
        [ {self.name} ] of {self.cname}
        {self.desc}
        """.lstrip("\n")