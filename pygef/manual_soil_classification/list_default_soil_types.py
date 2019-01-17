from collections import namedtuple

lithology = namedtuple('number', ['name','level_max', 'level_min', 'qc_max', 'qc_min', 'fn_max', 'fn_min'])

default_soil_types = {
    0: lithology(name='Veen',level_max=None, level_min=None, qc_max=2.0, qc_min=0.0, fn_max=12.0, fn_min=6.5),
    1: lithology(name='Klei_organisch',level_max=None, level_min=None, qc_max=2.0, qc_min=0.0, fn_max=6.5, fn_min=4.0),
    2: lithology(name='Klei',level_max=None, level_min=None, qc_max=1.5, qc_min=0.0, fn_max=4.0, fn_min=2.0),
    3: lithology(name='Cohesief_OC',level_max=None, level_min=None, qc_max=100.0, qc_min=2.0, fn_max=12.0, fn_min=2.0),
    4: lithology(name='Leem_klei_zandig',level_max=None, level_min=None, qc_max=3.0, qc_min=1.5, fn_max=4.0, fn_min=2.0),
    5: lithology(name='Klei_siltig_zandig',level_max=None, level_min=None, qc_max=2.0, qc_min=0.0, fn_max=2.0, fn_min=0.0),
    6: lithology(name='Zand_siltig_kleiig',level_max=None, level_min=None, qc_max=100.0, qc_min=2.0, fn_max=2.0, fn_min=1.0),
    7: lithology(name='Zand',level_max=None, level_min=None, qc_max=100.0, qc_min=2.0, fn_max=1.0, fn_min=0.0)
}

specified_soil_types_Rotterdam = {
    0: lithology(name='Antropogeen_veen', level_max=3.22, level_min=-4.00, qc_max=1.50, qc_min=0.0, fn_max=12.0, fn_min=5.5),
    1: lithology(name='Antrogeen_klei', level_max=3.22, level_min=-4.00, qc_max=2.50, qc_min=0.0, fn_max=5.5, fn_min=2.0),
    2: lithology(name='Antropogeen_zand', level_max=3.22, level_min=-4.00, qc_max=100, qc_min=2.0, fn_max=2.0, fn_min=0.0),
    3: lithology(name='Klei_humeaus_Naaldwijk', level_max=-4.00, level_min=-9.00, qc_max=1.0, qc_min=2.0, fn_max=5.5, fn_min=4.0),
    4: lithology(name='Klei_humeus_Echteld', level_max=-9.00, level_min=-30.00, qc_max=1.20, qc_min=0.0, fn_max=5.5, fn_min=3.5),
    5: lithology(name='Klei_siltig_Naaldwijk', level_max=-4.0, level_min=-9.0, qc_max=1.0, qc_min=0.0, fn_max=4.0, fn_min=1.0),
    6: lithology(name='Klei_siltig_Echteld',level_max=-9.0, level_min=-30.0, qc_max=1.0, qc_min=0.0, fn_max=3.5, fn_min=1.0),
    7: lithology(name='Klei_zandig',level_max=-4.0, level_min=-9.0, qc_max=2.0, qc_min=0.0, fn_max=3.0, fn_min=1.5),
    8: lithology(name='Hollandveen',level_max=-4.0, level_min=-9.0, qc_max=1.5, qc_min=0.0, fn_max=12.0, fn_min=5.5),
    9: lithology(name='Basisveen',level_max=-9.0, level_min=-30.0, qc_max=1.5, qc_min=0.0, fn_max=12.0, fn_min=5.5),
    10: lithology(name='Tussenzandlaag',level_max=-4.0, level_min=-11.5, qc_max=100.0, qc_min=2.0, fn_max=1.5, fn_min=0.0),
    11: lithology(name='Zand_pleictpceen',level_max=-11.5, level_min=-30.0, qc_max=100.0, qc_min=2.0, fn_max=1.5, fn_min=0.0)
}
