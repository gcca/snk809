## Proyecto Luci

### Objetivo

Asistir o Automatizar las actividades de hunters, kams y managers durante el ciclo de vida de los candidatos y empresas en los procesos de postulación profesional.

El ciclo de vida comprende el seguimiento de los candidatos para encontrar las empresas en las que sus habilidades pueden ser desarrolladas haciendo un análisis de sus habilidades blandas como desempeño técnico.

### Descripción técnica general

El proyecto Luci está desarrollado con el lenguaje Python utiliando el framework Django. Está desplegado usando un PasS con base de datos Mysql.

El esquema de desarrollo ágil está enfocado en features de alto nivel que se convierten en tareas técnicas registradas en el espacio de Github para la organización Snk809.

#### Ciclo de desarrollo

Los tableros de Github son usados para mapear épicas de desarrollo donde se establecen los objetivos funcionales en historias de usuarios descriptas como funcionalidades que debe cumplir la aplicación.

El equipo de desarrollo establece desgloces de las historias de usuario en tareas técnicas que forman parte de la planificación de desarrollo. Cada tablero busca reflejar el histórico de desarrollo y obtener información del equipo para identificar puntos de mejora con análisis de alto nivel.

Se utiliza los criterios de esfuerzo necesario, prioridad y complejidad técnica para representar el comportamiento del equipo. Esta información sirve para generar la velocidad media del equipo con la información recolectada semanalmente. Finalmente, se usa esta información para los siguientes desarrollos durante el ciclo de iteraciones de la épica.

### Arquitectura de la aplicación

#### Módulos

* sinek: perfil de candidatos.
* neodash: integra lo módulos usados por el hunter/kam/manager.
* onboard: invitar y obtener test de personalidad de los candidatos.
* quizzes: generar tests dinámicos para los candidatos.
* customers: especaio de interacción con los clientes.

![image](https://user-images.githubusercontent.com/143498/212110977-bdacbce7-4f62-4bc0-a033-86ca77ee1c41.png)

#### Desarrollo

Cada uno de los módulo definen un conjunto de views para acceder o implementar la ejecución de los casos de uso, los cuales trabajan con el modelo entidad relación propuesto por el framework. Adicionalmente, hay servicios de terceros que son usado mediante componentes creados para interactuar con los servicios web. Estos servicios son el correo electrónico, la autenticación con cuentas gmail y el almacenamiento de archivos de Google.

##### Onboard

![onboard](https://user-images.githubusercontent.com/143498/212112467-210e8e65-dce8-4f9a-be6d-e37983f508e6.png)

##### Quizzes

![question](https://user-images.githubusercontent.com/143498/212112580-7a373535-c059-4aef-81dc-e10fb0e855bf.png)
---
![answer](https://user-images.githubusercontent.com/143498/212112599-d7418cfc-c121-4da8-8b5a-0e5591eea34b.png)

##### Sinek

![freelancer1](https://user-images.githubusercontent.com/143498/212112752-58a72d30-1878-4348-b00c-2102516f2417.png)
---
![freelancer2](https://user-images.githubusercontent.com/143498/212112763-98351b5e-15de-4743-b9b4-3345331d58da.png)
---
![initiative](https://user-images.githubusercontent.com/143498/212112780-70c24cd2-7330-4445-bb6e-12d4a8e3f1ec.png)
