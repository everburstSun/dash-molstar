from typing import Dict, List, Optional, Union
import numpy as np

class Box(object):
    def __init__(self, min: tuple[float] = None, max: tuple[float] = None):
        self.__min = min
        self.__max = max
        self.__center = None
        self.__size = None
        if self.__min is not None and self.__max is not None:
            self.__center = ((self.__min[0] + self.__max[0]) / 2, (self.__min[1] + self.__max[1]) / 2, (self.__min[2] + self.__max[2]) / 2)
            self.__size = ((self.__max[0] - self.__min[0]), (self.__max[1] - self.__min[1]), (self.__max[2] - self.__min[2]))

    @property
    def min(self):
        if self.__min is not None:
            return self.__min
        return None

    @property
    def max(self):
        if self.__max is not None:
            return self.__max
        return None

    @property
    def center(self):
        if self.__center is not None:
            return self.__center
        return None

    @property
    def size(self):
        if self.__size is not None:
            return self.__size
        return None

    @property
    def min_x(self):
        if self.__min is not None:
            return self.__min[0]
        return None

    @property
    def min_y(self):
        if self.__min is not None:
            return self.__min[0]
        return None

    @property
    def min_z(self):
        if self.__min is not None:
            return self.__min[0]
        return None

    @property
    def max_x(self):
        if self.__max is not None:
            return self.__max[0]
        return None

    @property
    def max_y(self):
        if self.__max is not None:
            return self.__max[1]
        return None

    @property
    def max_z(self):
        if self.__max is not None:
            return self.__max[2]
        return None

    @property
    def size_x(self):
        if self.__size is not None:
            return self.__size[0]
        return None

    @property
    def size_y(self):
        if self.__size is not None:
            return self.__size[1]
        return None

    @property
    def size_z(self):
        if self.__size is not None:
            return self.__size[2]
        return None

    @property
    def center_x(self):
        if self.__center is not None:
            return self.__center[0]
        return None

    @property
    def center_y(self):
        if self.__center is not None:
            return self.__center[1]
        return None

    @property
    def center_z(self):
        if self.__center is not None:
            return self.__center[2]
        return None

    def to_sphere(self) -> 'Sphere':
        if self.__center is not None and self.__size is not None:
            center = self.__center
            radius = np.max(self.__size) / 2
            return Sphere(center, radius)
        return None

class Sphere(object):
    def __init__(self, center: tuple[float] = None, radius: float = None):
        self.__center = center
        self.__radius = radius

    @property
    def center(self):
        if self.__center is not None:
            return self.__center
        return None

    @property
    def radius(self):
        if self.__radius is not None:
            return self.__radius
        return None

    @property
    def center_x(self):
        if self.__center is not None:
            return self.__center[0]
        return None

    @property
    def center_y(self):
        if self.__center is not None:
            return self.__center[1]
        return None

    @property
    def center_z(self):
        if self.__center is not None:
            return self.__center[2]
        return None

    @property
    def radius_x(self):
        if self.__radius is not None:
            return self.__radius
        return None

    @property
    def radius_y(self):
        if self.__radius is not None:
            return self.__radius
        return None

    @property
    def radius_z(self):
        if self.__radius is not None:
            return self.__radius
        return None

    def to_box(self) -> Box:
        if self.__center is not None and self.__radius is not None:
            min = (self.__center[0] - self.__radius, self.__center[1] - self.__radius, self.__center[2] - self.__radius)
            max = (self.__center[0] + self.__radius, self.__center[1] + self.__radius, self.__center[2] + self.__radius)
            return Box(min, max)
        return None

class Boundary(object):
    def __init__(self, coords: np.ndarray = None):
        self.__box = None
        self.__sphere = None
        try:
            if coords is not None:
                min = (np.min(coords[:, 0]), np.min(coords[:, 1]), np.min(coords[:, 2]))
                max = (np.max(coords[:, 0]), np.max(coords[:, 1]), np.max(coords[:, 2]))
                center = ((min[0] + max[0]) / 2, (min[1] + max[1]) / 2, (min[2] + max[2]) / 2)
                radius = np.max(np.linalg.norm(coords - center, axis=1))
                self.__box = Box(min, max)
                self.__sphere = Sphere(center, radius)
        except:
            raise ValueError("Invalid coordinates provided to Boundary object")

    @property
    def box(self):
        return self.__box

    @property
    def sphere(self):
        return self.__sphere


class Atom(object):
    def __init__(self, index: int = None, name: str = None, x: float = None, y: float = None, z: float = None):
        self.__name = name
        self.__index = index
        self.__x = round(x, 6) if x is not None else None
        self.__y = round(y, 6) if y is not None else None
        self.__z = round(z, 6) if z is not None else None
        self.__valid = self.__index is not None

    @property
    def valid(self):
        return self.__valid

    @property
    def name(self):
        if not self.valid: return None
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def index(self):
        if not self.valid: return None
        return self.__index

    @index.setter
    def index(self, value):
        if isinstance(value, str):
            try:
                int_value = int(value)
                self.__index = int_value
                self.__valid = True
            except Exception:
                raise ValueError(f"Invalid number value: {value}")
        elif isinstance(value, int):
            self.__index = value
            self.__valid = True
        else:
            raise TypeError("number must be a string or integer")

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def z(self):
        return self.__z

class Residue(object):
    def __init__(self, index: int = None, number: int = None, ins_code: str = '', name: str = '', atoms: List['Atom'] = []):
        self.__name = name
        self.__index = index
        self.__number = number
        if index is not None and number is None:
            self.__number = index
        self.__ins_code = ins_code
        self.__atoms = []
        self.__parse_data(atoms)
        self.__valid = (self.__number is not None) or (self.__index is not None)

    def __len__(self):
        return len(self.__atoms)

    def __parse_data(self, atoms: List['Atom']):
        if atoms:
            for atom in atoms:
                name = atom.get('name', '')
                index = atom.get('index')
                x = atom.get('x')
                y = atom.get('y')
                z = atom.get('z')
                self.add_atom(index, name, x, y, z)

    @property
    def valid(self):
        return self.__valid

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def index(self):
        if not self.valid: return None
        return self.__index

    @index.setter
    def index(self, value):
        if isinstance(value, str):
            try:
                int_value = int(value)
                self.__index = int_value
                self.__valid = True
            except Exception:
                raise ValueError(f"Invalid number value: {value}")
        elif isinstance(value, int):
            self.__index = value
            self.__valid = True
        else:
            raise TypeError("number must be a string or integer")

    @property
    def number(self):
        if not self.valid: return None
        return self.__number

    @number.setter
    def number(self, value):
        if isinstance(value, str):
            try:
                int_value = int(value)
                self.__number = int_value
                self.__valid = True
            except Exception:
                raise ValueError(f"Invalid number value: {value}")
        elif isinstance(value, int):
            self.__number = value
            self.__valid = True
        else:
            raise TypeError("number must be a string or integer")

    @property
    def ins_code(self):
        return self.__ins_code

    @ins_code.setter
    def ins_code(self, value):
        self.__ins_code = value
        self.__valid = bool(value)

    @property
    def atoms(self) -> List[Atom]:
        return self.__atoms

    def find_atom(self, name: str) -> 'Atom':
        if not self.valid:
            raise ValueError('Cannot call find_atom on invalid Residue object')
        for atom in self.__atoms:
            if atom.name == name:
                return atom
        return Atom()

    def add_atom(self, index: int, name: str = None, x: float = None, y: float = None, z: float = None):
        atom = Atom(index, name, x, y, z)
        self.__atoms.append(atom)
    
    def remove_atom(self, name: Union[str, 'Atom']) -> bool:
        if isinstance(name, Atom):
            try:
                atom_index = self.__atoms.index(name)
                del self.__atoms[atom_index]
                return True
            except ValueError: pass
        else:
            atom = self.find_atom(name)
            if atom.valid:
                atom_index = self.__atoms.index(atom)
                del self.__atoms[atom_index]
                return True
        return False

class Chain(object):
    def __init__(self, chain_name: str = None, residues: List['Residue'] = [], auth_name: str = ''):
        self.__name = chain_name
        self.__auth_name = auth_name
        if chain_name and not auth_name:
            self.__auth_name = chain_name
        self.__residues = []
        self.__parse_data(residues)
        self.__valid = (self.__name is not None) or (self.__auth_name is not None)

    def __len__(self):
        return len(self.__residues)

    def __parse_data(self, residues: List['Residue']):
        if residues:
            for residue in residues:
                name = residue.get('name', '')
                index = residue.get('index')
                number = residue.get('number')
                ins_code = residue.get('ins_code', '')
                atoms = residue.get('atoms', [])
                self.add_residue(index, number, ins_code, name, atoms)

    @property
    def valid(self):
        return self.__valid

    @property
    def name(self):
        if not self.valid: return None
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value
        self.__valid = bool(value)

    @property
    def auth_name(self):
        if not self.valid: return None
        return self.__auth_name

    @auth_name.setter
    def auth_name(self, value):
        self.__auth_name = value
        self.__valid = bool(value)

    @property
    def residues(self) -> List[Residue]:
        return self.__residues

    @property
    def atoms(self) -> List[Atom]:
        atoms = []
        for residue in self.__residues:
            for atom in residue.atoms:
                if atom.valid:
                    atoms.append(atom)
        return atoms

    def find_residue(self, number, ins_code="") -> 'Residue':
        if not self.valid:
            raise ValueError('Cannot call find_residue on invalid Chain object')
        for residue in self.__residues:
            if residue.number == number and (residue.ins_code or "") == ins_code:
                return residue
        return Residue()

    def find_atom(self, residue_number, atom_name, ins_code="") -> 'Atom':
        if not self.valid:
            raise ValueError('Cannot call find_atom on invalid Chain object')
        residue = self.find_residue(residue_number, ins_code)
        if residue and residue.valid:
            return residue.find_atom(atom_name)
        return Atom()

    def add_residue(self, index: int, number: int = None, ins_code: str = '', name: str = '', atoms: List['Atom'] = []):
        residue = Residue(index, number, ins_code, name, atoms)
        self.__residues.append(residue)
    
    def remove_residue(self, number: Union[int, 'Residue'], ins_code: str = '') -> bool:
        if isinstance(number, Residue):
            try:
                residue_index = self.__residues.index(number)
                del self.__residues[residue_index]
                return True
            except ValueError: pass
        else:
            residue = self.find_residue(number, ins_code)
            if residue.valid:
                residue_index = self.__residues.index(residue)
                del self.__residues[residue_index]
                return True
        return False

class Target(object):
    def __init__(self, data: Dict = {}):
        self.__chains = []
        self.auth = False
        self.__parse_data(data)
        self.__boundary = None
        self.__valid = len(self.__chains) > 0

    def __len__(self):
        return len(self.__chains)

    def __parse_data(self, data: Dict):
        chains = data.get('chains', [])
        if chains:
            for chain in chains:
                chain_name = chain.get('name')
                auth_name = chain.get('auth_name', '')
                residues = chain.get('residues', [])
                self.add_chain(chain_name, residues, auth_name)

    @property
    def valid(self):
        return self.__valid

    @property
    def chains(self) -> List[Chain]:
        return self.__chains

    @property
    def residues(self) -> List[Residue]:
        residues = []
        for chain in self.__chains:
            for residue in chain.residues:
                if residue.valid:
                    residues.append(residue)
        return residues

    @property
    def atoms(self) -> List[Atom]:
        atoms = []
        for chain in self.__chains:
            for residue in chain.residues:
                for atom in residue.atoms:
                    if atom.valid:
                        atoms.append(atom)
        return atoms

    @property
    def boundary(self) -> Optional[Boundary]:
        if self.valid:
            if not self.__boundary:
                coords = np.array([[atom.x, atom.y, atom.z] for atom in self.atoms])
                self.__boundary = Boundary(coords)
            return self.__boundary
        raise ValueError('Cannot access boundary on invalid Target object')

    def find_chain(self, name) -> 'Chain':
        if not self.__valid:
            raise ValueError('Cannot call find_chain on invalid Target object')
        for chain in self.__chains:
            if chain.name == name:
                return chain
        return Chain()

    def find_residue(self, chain_name, residue_number, ins_code="") -> 'Residue':
        chain = self.find_chain(chain_name)
        if chain.valid:
            for residue in chain.residues:
                if residue.number == residue_number and (residue.ins_code or "") == ins_code:
                    return residue
        return Residue()

    def find_atom(self, chain_name, residue_number, atom_name, ins_code="") -> 'Atom':
        chain = self.find_chain(chain_name)
        if chain.valid:
            residue = chain.find_residue(residue_number, ins_code)
            if residue.valid:
                return residue.find_atom(atom_name)
        return Atom()

    def add_chain(self, chain_name: str, residues: List = [], auth_name: str = ''):
        chain = Chain(chain_name, residues, auth_name)
        self.__chains.append(chain)
        self.__valid = True

    def remove_chain(self, chain_name: Union[str, 'Chain']) -> bool:
        if isinstance(chain_name, Chain):
            try:
                chain_index = self.__chains.index(chain_name)
                del self.__chains[chain_index]
                if not self.__chains:
                    self.__valid = False
                return True
            except ValueError: pass
        else:
            chain = self.find_chain(chain_name)
            if chain.valid:
                chain_index = self.__chains.index(chain)
                del self.__chains[chain_index]
                if not self.__chains:
                    self.__valid = False
                return True
        return False
    
    def to_dict(self) -> Dict:
        data = {
            'chains': [],
            'auth': self.auth
        }
        for chain in self.__chains:
            chain_data = {
                'name': chain.name,
                'auth_name': chain.auth_name,
                'residues': []
            }
            for residue in chain.residues:
                residue_data = {
                    'name': residue.name,
                    'index': residue.index,
                    'number': residue.number,
                    'ins_code': residue.ins_code,
                    'atoms': []
                }
                for atom in residue.atoms:
                    atom_data = {
                        'name': atom.name,
                        'index': atom.index,
                        'x': atom.x,
                        'y': atom.y,
                        'z': atom.z
                    }
                    residue_data['atoms'].append(atom_data)
                chain_data['residues'].append(residue_data)
            data['chains'].append(chain_data)
        return data

if __name__ == "__main__":
    sample_data = {'chains': [{'name': 'L', 'auth_name': 'L', 'residues': [{'name': 'GLY', 'index': 62, 'number': 62, 'ins_code': '', 'atoms': [{'name': 'N', 'index': 4817, 'x': 3.759000062942505, 'y': -11.343000411987305, 'z': -5.960999965667725}, {'name': 'CA', 'index': 4818, 'x': 4.876999855041504, 'y': -12.213000297546387, 'z': -6.27400016784668}, {'name': 'C', 'index': 4819, 'x': 6.201000213623047, 'y': -11.520999908447266, 'z': -6.026000022888184}, {'name': 'O', 'index': 4820, 'x': 6.288000106811523, 'y': -10.29699993133545, 'z': -6.059000015258789}]}, {'name': 'ASN', 'index': 133, 'number': 133, 'ins_code': '', 'atoms': [{'name': 'N', 'index': 5366, 'x': -15.53499984741211, 'y': -41.314998626708984, 'z': 11.765999794006348}, {'name': 'CA', 'index': 5367, 'x': -16.469999313354492, 'y': -40.20199966430664, 'z': 11.64799976348877}, {'name': 'C', 'index': 5368, 'x': -16.136999130249023, 'y': -38.9630012512207, 'z': 12.482000350952148}, {'name': 'O', 'index': 5369, 'x': -15.72700023651123, 'y': -39.069000244140625, 'z': 13.640000343322754}, {'name': 'CB', 'index': 5370, 'x': -17.892000198364258, 'y': -40.66999816894531, 'z': 11.961000442504883}, {'name': 'CG', 'index': 5371, 'x': -18.92799949645996, 'y': -39.95800018310547, 'z': 11.12399959564209}, {'name': 'OD1', 'index': 5372, 'x': -18.735000610351562, 'y': -39.75400161743164, 'z': 9.925000190734863}, {'name': 'ND2', 'index': 5373, 'x': -20.030000686645508, 'y': -39.5620002746582, 'z': 11.75100040435791}]}]}, {'name': 'H', 'auth_name': 'H', 'residues': [{'name': 'ARG', 'index': 105, 'number': 99, 'ins_code': 'B', 'atoms': [{'name': 'N', 'index': 825, 'x': 1.0479999780654907, 'y': -5.711999893188477, 'z': -34.37200164794922}, {'name': 'CA', 'index': 826, 'x': 2.497999906539917, 'y': -5.5329999923706055, 'z': -34.34299850463867}, {'name': 'C', 'index': 827, 'x': 3.2239999771118164, 'y': -6.763000011444092, 'z': -33.80699920654297}, {'name': 'O', 'index': 828, 'x': 4.064000129699707, 'y': -7.335999965667725, 'z': -34.49399948120117}, {'name': 'CB', 'index': 829, 'x': 2.881999969482422, 'y': -4.296999931335449, 'z': -33.5260009765625}, {'name': 'CG', 'index': 830, 'x': 2.4560000896453857, 'y': -2.9779999256134033, 'z': -34.152000427246094}, {'name': 'CD', 'index': 831, 'x': 2.986999988555908, 'y': -1.7869999408721924, 'z': -33.358001708984375}, {'name': 'NE', 'index': 832, 'x': 4.429999828338623, 'y': -1.6050000190734863, 'z': -33.513999938964844}, {'name': 'CZ', 'index': 833, 'x': 4.988999843597412, 'y': -0.7549999952316284, 'z': -34.37200164794922}, {'name': 'NH1', 'index': 834, 'x': 4.22599983215332, 'y': -0.003000000026077032, 'z': -35.154998779296875}, {'name': 'NH2', 'index': 835, 'x': 6.309999942779541, 'y': -0.6520000100135803, 'z': -34.446998596191406}]}, {'name': 'GLY', 'index': 116, 'number': 108, 'ins_code': '', 'atoms': [{'name': 'N', 'index': 942, 'x': -10.392000198364258, 'y': -21.732999801635742, 'z': -22.767000198364258}, {'name': 'CA', 'index': 943, 'x': -11.680999755859375, 'y': -22.361000061035156, 'z': -22.992000579833984}, {'name': 'C', 'index': 944, 'x': -12.182999610900879, 'y': -22.957000732421875, 'z': -21.683000564575195}, {'name': 'O', 'index': 945, 'x': -11.437999725341797, 'y': -23.02899932861328, 'z': -20.70199966430664}]}, {'name': 'CYS', 'index': 204, 'number': 200, 'ins_code': '', 'atoms': [{'name': 'N', 'index': 1558, 'x': -31.833999633789062, 'y': -45.24300003051758, 'z': 0.6779999732971191}, {'name': 'CA', 'index': 1559, 'x': -30.711000442504883, 'y': -44.742000579833984, 'z': -0.10599999874830246}, {'name': 'C', 'index': 1560, 'x': -31.20800018310547, 'y': -44.34600067138672, 'z': -1.4950000047683716}, {'name': 'O', 'index': 1561, 'x': -31.722000122070312, 'y': -45.1870002746582, 'z': -2.2300000190734863}, {'name': 'CB', 'index': 1562, 'x': -29.65999984741211, 'y': -45.847999572753906, 'z': -0.23800000548362732}, {'name': 'SG', 'index': 1563, 'x': -27.940000534057617, 'y': -45.314998626708984, 'z': -0.17599999904632568}]}]}]}
    target = Target(sample_data)
    print("Target valid:", target.valid)
    print("Number of chains:", len(target))
    for chain in target.chains:
        print("Chain name:", chain.name, ",Auth name:", chain.auth_name)
        for residue in chain.residues:
            print("  Residue index:", residue.index, ",Residue number:", str(residue.number)+residue.ins_code, ",Name:", residue.name)
            for atom in residue.atoms:
                print("    Atom name:", atom.name, ",x:", atom.x, ",y:", atom.y, ",z:", atom.z)
    print("Number of chains:", len(target))
    print("Number of residues:", len(target.residues))
    print("Number of atoms:", len(target.atoms))
    print("Finding atom:", target.find_atom('H', 99, 'N', 'B').valid) # True
    print("Finding residue:", target.find_residue('L', 71).valid) # False
    print("Finding chain:", target.find_chain('L').valid)  # True
    print("Finding chain:", target.find_chain('X').valid)  # False
    print("Finding residue:", target.find_residue('X', 71).valid)  # False
    residue = target.find_residue('H', 99, 'B')
    CA = residue.find_atom('CA')
    CB = residue.find_atom('CB')
    print("Finding atom CA:", CA.valid) # True
    print("Finding atom CB:", CB.valid) # True
    residue.remove_atom('CA')
    residue.remove_atom(CB)
    print("Finding atom CA after remove:", residue.find_atom('CA').valid) # False
    print("Finding atom CB after remove:", target.find_atom('H', 99, 'CB', 'B').valid) # False
    print("Boundary box min:", target.boundary.box.min)
    print("Boundary box max:", target.boundary.box.max)
    print("Boundary sphere center:", target.boundary.sphere.center)
    print("Boundary sphere radius:", target.boundary.sphere.radius)