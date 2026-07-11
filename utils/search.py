class Searchable:
    def relevant_orth(self):
        if hasattr(self, "orth") and self.orth is not None:
            return self.orth
        else:
            return self.radical.orth
        
    def to_searchable(self, orth=None, root_orth=None, meanings=None, origin_of_tongue=None):
        data = {}
        data["orth"] = orth if orth else self.relevant_orth()
        data["root_orth"] = root_orth if root_orth else self.radical.orth if hasattr(self, "radical") else None
        data["meanings"] = meanings if meanings else self.radical.meanings if hasattr(self, "radical") else None
        data["origin_of_tongue"] = origin_of_tongue if origin_of_tongue else self.radical.origin_of_tongue.value if hasattr(self, "radical") else None
        return data
