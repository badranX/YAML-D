FIRST_CHAR2TYPES = {

    '[': list,
    '"': str,
    "'": str,
}

LIST_CAST_TYPES = {
    (int, float): float,
    (float, int): float
}


def _ylist_type_cast(old_types, new_types):
    def c(fromto):
        from_type, to_type = fromto
        if from_type == to_type:
            return from_type
        else:
            new_type =  LIST_CAST_TYPES.get(fromto, False)
            if not new_type:
                raise Exception(f'List type error, tyring to cast {from_type} to {to_type}')
            return new_type
    
    return map(c, zip(old_types.values(), new_types.values()))

class Read():
    def __init__(self, backend, is_onelist=False, tgt_parent=None):
        self.backend = backend
        self.is_onelist = is_onelist
        self.tgt_parent = tgt_parent
        
        #init read
        self.out = None
        self.current_parent = None
        self.list_counter = 0
        self.yaml_obj = dict()
        self.yaml_obj_types = dict()
        self.all_types = dict()
        self.list_counter = 0

        #line level 
        self.key = None
        self.value = None
        self.is_parent = False
        self.is_child = False
        self.is_minus = False
        self.is_obj_parsing_done = False
    
    def _reset(self):
        #reset and skip
        if self.is_parent:
            if self.is_onelist and self.list_counter:
                raise Exception("You specified a one list('-') yaml2d file but a key was found after parsing the list")
            self.current_parent = self.key
            self.list_counter = 0
            
        if self.is_obj_parsing_done:
            self.yaml_obj = dict()
            self.yaml_obj_types = dict()
            


    def process_line(self, line):
        striped_line = line.strip()
        if not striped_line:
            return None

        self.is_child = line[0].isspace()
        self.is_parent = not self.is_child
        line = striped_line

        key, value = line.strip().split(':', 1)
        self.key, self.value = key.strip(), value.strip()

        self.is_minus = key[0] == '-'
        self.is_obj_parsing_done = (self.is_parent or self.is_minus) and bool(self.yaml_obj)
        
        
    def parsing_obj(self):
        #record current line if not parent
        if self.is_minus:
            self.list_counter += 1
            self.key = self.key[1:].strip()
        self.yaml_obj[self.key] = self.value
        ytype = FIRST_CHAR2TYPES.get(self.value[0], False)
        if not ytype:
            ytype = float if '.' in self.value else int
        self.yaml_obj_types[self.key] = ytype

    def _backend(self, is_last):
        #write previous object to the self.backend if done parsing
        if self.is_obj_parsing_done:
            if self.list_counter and self.current_parent in self.all_types:
                new_obj_types = self.all_types[self.current_parent]
                new_obj_types = _ylist_type_cast(self.all_types[self.current_parent], self.yaml_obj_types)
                self.yaml_obj_types = dict(zip(self.yaml_obj_types.keys(), new_obj_types))
            self.all_types[self.current_parent] = self.yaml_obj_types
            self.out = self.backend(self.out, False, self.current_parent, self.yaml_obj, self.list_counter, self.all_types)
            if is_last:
                self.out = self.backend(self.out, True, None, None, None, self.all_types)

    def read(self, lines):
        for line in lines:
            self.process_line(line)
            self._backend(False)
            self._reset()
            if self.is_child:
                self.parsing_obj()
        self.is_obj_parsing_done = True
        self._backend(True)
        return self.out

    def read(self, lines):
        for line in lines:
            self.process_line(line)
            self._backend(False)
            self._reset()
            if self.is_child:
                self.parsing_obj()
        self.is_obj_parsing_done = True
        self._backend(True)
        return self.out


    def read_generator(self, lines):
        for line in lines:
            self.process_line(line)
            self._backend(False)
            yield self.out
            self._reset()
            if self.is_child:
                self.parsing_obj()
        self.is_obj_parsing_done = True
        self._backend(True)
        yield self.out


if __name__ == "__main__":
    pass
