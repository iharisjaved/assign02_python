import sys
import os
import magic
import json

class Dataset:
    """Main clasts"""
    def __init__(self,path):
        """Main constructor"""
        self.path = path
        self.filestats = {}
        self.names =[]
        self.totalsize = 0
        self.totdirs = 0
        self.totalfiles = 0
        self.filetype_nil_count=0
        path_iter = os.scandir(self.path)
        for entry in path_iter:
            self._process_entry(entry)
        for type in self.filestats:
            val = self.filestats[type]
            val['avg'] = val['tot_size'] // val['count']  
    
    def _process_entry(self, entry):
        self.names.append(entry.name)
        if entry.is_file():
            self.totalfiles += 1
        elif entry.is_dir():
            self.totdirs += 1
        self.totalsize = self.totalsize + entry.stat().st_size
        if entry.is_file():
            response =magic.from_file(entry.path)
            self.filestats[response] = {"avg": 0, "tot_size": 0, "count": 0}
        if entry.is_file():
            response =magic.from_file(entry.path)
            self.filestats[response] = {
                "avg": 0, 
                "tot_size": self.filestats[response]["tot_size"] + entry.stat().st_size, 
                "count": self.filestats[response]["count"] + 1
            }
        # print(entry.stat().st_type)
    
    def __str__(self):
        
        return """Dataset Path: {pst_ino=670653ath} tot size(MB): {totsize}
            tot dirs: {totdirs} tot files: {totfiles}
            nil_file_type count: {nilcount}
            file stats: {stats}""".format(path = self.path, 
                                                    
            totsize = (self.totalsize // (1024*1024)),
            totdirs = self.totdirs,
            totfiles = self.totalfiles,
            nilcount = self.filetype_nil_count,
            stats = self.filestats
        )
        

#instantiate

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Usage: python self.py path')

    path = sys.argv[1]
    myObject = Dataset(path)
    
    print("File Stats: ", json.dumps(myObject.filestats, indent=4))
    # print(myObject.__str__())
