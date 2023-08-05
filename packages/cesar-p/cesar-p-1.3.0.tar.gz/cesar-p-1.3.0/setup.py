# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cesarp',
 'cesarp.SIA2024',
 'cesarp.SIA2024.demand_generators',
 'cesarp.common',
 'cesarp.common.profiles',
 'cesarp.common.typing',
 'cesarp.construction',
 'cesarp.emissons_cost',
 'cesarp.energy_strategy',
 'cesarp.eplus_adapter',
 'cesarp.geometry',
 'cesarp.graphdb_access',
 'cesarp.idf_constructions_db_access',
 'cesarp.manager',
 'cesarp.model',
 'cesarp.operation',
 'cesarp.operation.fixed',
 'cesarp.results',
 'cesarp.retrofit',
 'cesarp.retrofit.all_bldgs',
 'cesarp.retrofit.embodied',
 'cesarp.retrofit.energy_perspective_2050',
 'cesarp.site',
 'cesarp.weather',
 'cesarp.weather.swiss_communities',
 'cesarp.weather.swiss_communities.ressources']

package_data = \
{'': ['*'],
 'cesarp.SIA2024': ['generated_params/nominal/*',
                    'generated_params/variable/*'],
 'cesarp.energy_strategy': ['ressources/business_as_usual/efficiencies/*',
                            'ressources/business_as_usual/energymix/*',
                            'ressources/business_as_usual/fuel/*',
                            'ressources/business_as_usual/retrofit/*',
                            'ressources/general/*',
                            'ressources/new_energy_policy/efficiencies/*',
                            'ressources/new_energy_policy/energymix/*',
                            'ressources/new_energy_policy/fuel/*',
                            'ressources/new_energy_policy/retrofit/*'],
 'cesarp.eplus_adapter': ['ressources/*'],
 'cesarp.graphdb_access': ['ressources/*'],
 'cesarp.idf_constructions_db_access': ['ressources/*',
                                        'ressources/IDFConstructions/*'],
 'cesarp.operation.fixed': ['ressources/*'],
 'cesarp.retrofit.embodied': ['ressources/*'],
 'cesarp.retrofit.energy_perspective_2050': ['ressources/*'],
 'cesarp.weather.swiss_communities.ressources': ['weather_files/*']}

install_requires = \
['PyYaml>=5.1.2,<6.0.0',
 'SPARQLWrapper>=1.8.5,<2.0.0',
 'Shapely>=1.7.1,<2.0.0',
 'eppy>=0.5.52,<0.6.0',
 'esoreader>=1.2.3,<2.0.0',
 'jsonpickle==1.3',
 'numpy>=1.16.5,<2.0.0',
 'pandas>=0.25.1,<0.26.0',
 'pint>=0.10.1,<0.11.0',
 'python-contracts>=0.1.4,<0.2.0',
 'rdflib>=4.2.2,<5.0.0',
 'scipy>=1.5.2,<2.0.0',
 'xlrd>=1.2.0,<2.0.0']

extras_require = \
{'geopandas': ['geopandas>=0.7.0,<0.8.0']}

setup_kwargs = {
    'name': 'cesar-p',
    'version': '1.3.0',
    'description': 'Combined Energy Simulation And Retrofit',
    'long_description': '**CESAR-P** stands for **C**ombined **E**nergy **S**imulation **A**nd **R**etrofit in **P**yhton.\n\nThe package allows for simulating the building **energy demand of a district**, including options for retrofitting, cost and emission calculation. The energy demand simulated includes:\n\n- heating\n- domestic hot water\n- cooling\n- electricity\n\nThe tool was developed at **Urban Energy Systems Lab**, which is part of the Swiss Federal Laboratories for Materials Science and Technology (Empa).\n\nFor more details please have a look at the documentation. A good starting point for general information is the README section.',
    'author': 'Leonie Fierz',
    'author_email': 'leonie.fierz@empa.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hues-platform/cesar-p-core',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
