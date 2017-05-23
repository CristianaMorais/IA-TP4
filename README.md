# Decision Trees
## Inteligencia Artificial - 2017
Implementação do algorimto ID3 em Python3. O algoritmo encontra-se preparado para receber um conjunto de dados exmplo através de um csv. Caso existam atributos que sejam numéricos, de forma automática são traduzidos em classes de forma a simplificar a árvore de decisão. Os casos para testes também são passsados ao programa utilizando ficheiros csv.
### Funcionamento
````
 $ python3 main.py [-h] [-e EXAMPLES] [-p] [-t TESTES]
````
##### Argumentos:
  * -h, --help
    >show this help message and exit
  * -e EXAMPLES, --examples EXAMPLES
    >Documento com os dados que queremeos que a máquina                aprenda.
  * -p, --print
    >Imprimir a árvore de decisão.
  * -t TESTES, --testes TESTES
    >Documentos onde se encontram os dados que se prentende avaliar.

#### Requesitos:
Para poder utilizar o programa é necessário os seguintes módulos:
* csv
* math
* sys
* copy
* argparse

----

O projeto foi testado em:
* Arch Linux, Python 3.6.1, GCC 6.3.1.
* Windows 10, Python 3.6.0.

##### Trabalho realizado por:
###### [André Cirne](https://sigarra.up.pt/fcup/pt/fest_geral.cursos_list?pv_num_unico=201505860)
###### [José Sousa](https://sigarra.up.pt/fcup/pt/fest_geral.cursos_list?pv_num_unico=201503443)
