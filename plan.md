La idea actual es investigar repositorios como el de nanobot y construir nuestro propio agente con un loop (empezamos con ReAct) intentnado que sea lo mas simple posible

Tenemos que permitirle que guarde cosas en memoria, pero no quiero complicarlo, al final el tema del contexto es muy importante en los agentes, cuanto mas peor

Tiene que poder comunicarse via codigo a poder ser

Me gusta la idea de que se construya sus propias skills, tools y demas

Me gusta la idea de poder comunicarte con el con comandos

Me gusta la idea de que tenga la capcidad de hacer Cron

Si bien hay que dejarle bash, deberiamos usar algun tipo de restricted bash para que no pueda hacer barbaridades ni tampoco leer cosas que no deberia.

Creo que las tools "basicas" que interactuen con tu PC deberian limitarle. Luego cuidado porque se podria hacer tools que rompan tu PC xddddd -> restricted Python?