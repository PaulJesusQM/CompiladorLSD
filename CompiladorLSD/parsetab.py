
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'ACORDE BPM CLAVE COMA DURACION NOTA PAUSApentagrama : config compasconfig : CLAVE BPMcompas : compas notacion\n              | notacionnotacion : notacion elemento\n                | elementoelemento : nota\n                | acorde\n                | pausanota : NOTA COMA DURACIONacorde : ACORDE COMA DURACIONpausa : PAUSA COMA DURACION'
    
_lr_action_items = {'CLAVE':([0,],[3,]),'$end':([1,4,5,6,7,8,9,14,15,19,20,21,],[0,-1,-4,-6,-7,-8,-9,-3,-5,-10,-11,-12,]),'NOTA':([2,4,5,6,7,8,9,13,14,15,19,20,21,],[10,10,10,-6,-7,-8,-9,-2,10,-5,-10,-11,-12,]),'ACORDE':([2,4,5,6,7,8,9,13,14,15,19,20,21,],[11,11,11,-6,-7,-8,-9,-2,11,-5,-10,-11,-12,]),'PAUSA':([2,4,5,6,7,8,9,13,14,15,19,20,21,],[12,12,12,-6,-7,-8,-9,-2,12,-5,-10,-11,-12,]),'BPM':([3,],[13,]),'COMA':([10,11,12,],[16,17,18,]),'DURACION':([16,17,18,],[19,20,21,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'pentagrama':([0,],[1,]),'config':([0,],[2,]),'compas':([2,],[4,]),'notacion':([2,4,],[5,14,]),'elemento':([2,4,5,14,],[6,6,15,15,]),'nota':([2,4,5,14,],[7,7,7,7,]),'acorde':([2,4,5,14,],[8,8,8,8,]),'pausa':([2,4,5,14,],[9,9,9,9,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> pentagrama","S'",1,None,None,None),
  ('pentagrama -> config compas','pentagrama',2,'p_pentagrama','compilador.py',64),
  ('config -> CLAVE BPM','config',2,'p_config','compilador.py',68),
  ('compas -> compas notacion','compas',2,'p_compas','compilador.py',72),
  ('compas -> notacion','compas',1,'p_compas','compilador.py',73),
  ('notacion -> notacion elemento','notacion',2,'p_notacion','compilador.py',80),
  ('notacion -> elemento','notacion',1,'p_notacion','compilador.py',81),
  ('elemento -> nota','elemento',1,'p_elemento','compilador.py',88),
  ('elemento -> acorde','elemento',1,'p_elemento','compilador.py',89),
  ('elemento -> pausa','elemento',1,'p_elemento','compilador.py',90),
  ('nota -> NOTA COMA DURACION','nota',3,'p_nota','compilador.py',94),
  ('acorde -> ACORDE COMA DURACION','acorde',3,'p_acorde','compilador.py',98),
  ('pausa -> PAUSA COMA DURACION','pausa',3,'p_pausa','compilador.py',102),
]