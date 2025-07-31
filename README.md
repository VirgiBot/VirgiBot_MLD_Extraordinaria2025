<h1 align="center">VIRGIBOT - Propuesta de asistente conversacional para el Máster en Letras Digitales</h1>

<p align="center">
  VirgiBot es un asistente conversacional construido en la plataforma <em>IBM Watsonx Assistant</em> que se encarga de resolver consultas relativas al Máster en Letras Digitales de la Universidad Complutense de Madrid. Para ello, utiliza un modelo híbrido tanto proporcionando respuestas estáticas a través de la plataforma IBM Watsonx Assistant como generativas a través de modelos alojados en Groq.
</p>  
<p align="center">
  Esta propuesta constituye el producto desarrollado en el TFM "VIRGIBOT. PROPUESTA DE UN ASISTENTE CONVERSACIONAL PARA LA PÁGINA WEB DEL MÁSTER UNIVERSITARIO EN LETRAS DIGITALES", cuyo autor es Daniel Prado y sus tutores Juan Antonio Clemente y Sandra Miguel.
</p>

## 📚 Tabla de contenidos

- [📌 Introducción](#introducción)
- [🧱 Componentes y estructura](#componentes-y-estructura)
- [⚙️ Replicación paso a paso](#replicación-paso-a-paso)
- [📜 Contacto](#contacto)

---

<h2>📌 INTRODUCCIÓN</h2>

<p>
Este repositorio contiene todos los elementos necesarios para desplegar una instancia de <strong>VirgiBot</strong>. Como parte de mi Trabajo de Fin de Máster (TFM), he desarrollado un agente conversacional completamente funcional que ofrece respuestas a consultas sobre el <strong>Máster en Letras Digitales (MLD)</strong>. La información que maneja VirgiBot se basa en la presente en la página oficial del MLD (<a href="https://www.ucm.es/master-letrasdigitales">https://www.ucm.es/master-letrasdigitales</a>), y en algunos casos se complementa o amplía gracias a las capacidades de un modelo de inteligencia artificial generativa.
</p>

<p>
VirgiBot está construido sobre la plataforma <strong>IBM Watsonx Assistant</strong>, que contiene su base de conocimiento. Esto quiere decir que se encarga de realizar el reconocimiento de <em>intents</em> (intenciones del usuario), <em>entities</em> (elementos clave dentro de las frases) y de ofrecer respuestas basadas en flujos conversacionales predefinidos. Para la mayoría de consultas, las respuestas son estáticas y gestionadas dentro de Watsonx. Sin embargo, para ciertos <em>intents</em> seleccionados, se ha implementado un sistema de generación dinámica conectado a través de un <em>webhook</em>. 
</p>

<p>
El desarrollo completo, las decisiones de diseño, la arquitectura del agente y la evaluación de su rendimiento están documentados en detalle en el TFM.
</p>

---

<h2>🧱 COMPONENTES Y ESTRUCTURA</h2>

<p>
Este repositorio tiene la siguiente estructura.
</p>

```
📁 VirgiBot_MLD/
├── 📁 Chatbot_IBMWatson/       # Base de conocimiento del bot en formato JSON
│   └── 📄 VirgiBot.json        # Estructura JSON del bot para importar en Watsonx
├── 📁 GenAI_Code/              # Código para la generación de respuestas
│   ├── 📄 requirements.txt     # Lista de dependencias
│   ├── 📄 app.py               # App Flask que genera respuestas con IA generativa
│   └── 📄 función_calendario.py# Función para el intent WEB-Calendario
├── 📁 Métricas/                # Evaluación del rendimiento del chatbot
│   └── 📄 KPIs.xlsx            # Análisis de entendimiento
└── 📄 README.md                # Documentación del proyecto
```


<p>
La base de conocimiento de <strong>VirgiBot</strong> está implementada en <strong>IBM Watsonx Assistant</strong>, donde se han definido los <em>intents</em>, <em>entities</em> y las respuestas estáticas del asistente. Esta configuración permite cubrir interacciones frecuentes con respuestas controladas. Seis casos de uso se resuelven con respuestas estáticas.
</p>

<p>
No obstante, para dos <em>intents</em> se opta por una generación dinámica de respuestas utilizando un modelo de <strong>IA generativa</strong>. Para ello se utiliza una pequeña aplicación Flask ubicada en la carpeta <code>GenAI_Code</code>, que se encarga de recibir la entrada del usuario y generar una respuesta personalizada.
</p>

<p>
Esta aplicación debe ser desplegada en la nube (por ejemplo, en Render) y conectada con Watsonx Assistant mediante un <strong>webhook</strong>. Un webhook es un punto de conexión HTTP al que Watson puede enviar peticiones con el texto del usuario, y desde el cual recibe la respuesta que finalmente entrega al usuario.
</p>

<p>
La carpeta <code>Métricas</code> contiene documentación y resultados de la evaluación del rendimiento del chatbot, incluyendo análisis de cobertura, precisión de los intents y la calidad de las respuestas generadas.
</p>

<h2>⚙️ REPLICACIÓN PASO A PASO</h2>

<p>
A continuación, se propone una guía para replicar VirgiBot tal y como ha sido desarrollado para este TFM, incluyendo su estructura funcional básica, para probarlo tanto a nivel local como en la nube. Este asistente se ha desarrollado persiguiendo la posibilidad de desplegarlo de manera totalmente gratuita, lo cual es posible en estos términos pero bajo un tráfico de visitantes limitado. Además, dependiendo del lugar de despliegue (por ejemplo, si se aloja en una página web propia institucional), elementos como la dirección del webhook pueden ser sustituidos.
</p>

<h3> Registro y creación de cuentas </h3>

<p>
En primer lugar, para desplegar VirgiBot, se requiere el registro en diferentes plataformas.
- <strong><a href="https://www.ibm.com/es-es/products/watsonx-assistant?lnk=flatitem"> IBM Watsonx Assistant </a></strong>: Creación de cuenta en IBM Cloud y de instancia en IBM Watsonx Assistant con el plan gratuito <em>Lite</em>, que permite la gestión de un asistente conversacional funcional con ciertos límites de uso simultáneo y peticiones. En el caso de que se superasen estos límites, se permite la creación de una cuenta de pago por uso. <br>
- <strong><a href="https://console.groq.com/home"> Groq </a></strong>: Creación de cuenta gratuita (nivel <em>Free</em>) y obtención de <em>API KEY </em> (clave que permite la conexión a sus servidores), que permite la llamada a modelos de inteligencia artifical generativa alojados en sus servidores bajo unos límites de uso. De igual manera, si se necesitasen superar estos límites, también existe la posibilidad de crear una cuenta de pago por uso. <br>
- <strong>GitHub</strong>: para clonar el código y realizar las modificaciones que se estimen oportunas siguiendo un control de cambios. Además, numerosos servicios como Render permiten la integración con GitHub, por ejemplo para desplegar automáticamente cada actualización que se produzca en el código alojado en este servicio. <br>
OPCIONAL: <br>
- <strong>Render</strong>: Render permite alojar una aplicación o servicio en sus servidores y proporciona una dirección URL para realizar las llamadas al mismo. Es decir, proporciona la URL hacia la que el agente conversacional envía el mensaje del usuario en dos <em> intents </em> específicos, ejecuta el código desarrollado en la nube, y devuelve el resultado. Si se pretende desplegar el asistente en un servidor propio, este paso es innecesario. 
</p>

<h3>Importación en IBM Watsonx Assistant </h3>
<p> Tras la creación de la cuenta en IBM Cloud, se debe crear una instancia de Watsonx Assistant y completar el formulario de detalles de creación del bot, seleccionando el nombre "VirgiBot" y los colores "FFFF" y "LALALA" como principales y secundarios respectivamente. </p>
<p> A continuación, una vez inicializado el asistente, es necesario dirigirse al menú <code> Options </code> y activar la opción <code> Dialogs </code> (en lugar de <code>Actions</code>), que permite un control más detallado del flujo conversacional mediante nodos encadenados, como se ha planteado en este proyecto. </p>

<p> Finalmente, se debe simplemente acceder al menú <code> Upload / Download </code> y cargar en la interfaz el archivo VirgiBot.json que se encuentra en la carpeta <code> Chatbot_IBMWatson </code> de este repositorio. El asistente estará completamente cargado y estará disponible para su pruena con sus <em> intents </em> estáticos.

<h3>Clonación en GitHub</h3>

<p> A continuación, se debe clonar este repositorio a través del comando <code> git clone url </code> o desde la interfaz de GitHub. Tras copiarlo y alojarlo en una cuenta propia, se debe completar el archivo <code>.env</code> con la API KEY de Groq (GROQ_API_KEY), que se obtiene en el siguiente paso.

<h3>Obtención de API KEY de Groq</h3>
<p> Tras registrarse en Groq, hay que dirigirse a la consola y a la sección de API KEYS de <a href="https://console.groq.com/keys"> GroqCloud </a>. Ahí, se obtiene una clave <strong> única y privada </strong> que se debe asignar en el archivo <code>.env</code> del repositorio.

<h3> Despliegue del código del repositorio en un servidor </h3>
<p>Por último, para que VirgiBot pueda comunicarse con el código de este repositorio para lanzar cuestiones y recibir respuestas para los dos <em> intents </em> resueltos por IA Generativa, es necesario que esté alojado en un servidor que proporcione una dirección HTTP.</p>
<p> Si no se dispone de servidor propio, puede crearse uno gratuito bajo ciertos límites de uso en Render. Basta conectar una instancia a la dirección de GitHub para que se pueda ejecutar en la nube. Toda API KEY necesaria (en este caso, la de Groq) debe proporcionarse también al servidor para que pueda ejecutar el código.

<p><strong>IMPORTANTE</strong></p>
<p> Hay que cambiar la URL del <em> webhook </em> por la que se vaya a utilizar. En este repositorio, la URL de ejemplo es la que se usó para la evaluación del asistente y ya no se encuentra disponible. Es esencial disponer de esta dirección para que el agente tenga una funcionalidad completa. Una vez se disponga de esta dirección, hay que cambiarla en el apartado <code> Webhooks </code> dentro de IBM Watsonx Assistant.

<h3>Integración en página web</h3>
Como último paso, se debe utilizar el <em>widget</em> o las integraciones de Watsonx Assitant para colocar el asistente en una página web. Dependiendo de las necesidades del instalador, se empleará una u otra opción. Estas opciones se encuentran en el apartado <code> Publish </code> dentro de Watsonx.

<h2>📜Contacto</h2>
Este asistente ha sido desarrollado por <a href="https://www.linkedin.com/in/daniel-prado-aranda/"> Daniel Prado Aranda</a> como parte de su TFM para el Máster en Letras Digitales de la Universidad Complutense de Madrid en el curso académico 2024/25.

