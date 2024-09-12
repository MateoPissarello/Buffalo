def suma():
cuantos_sum=int(input("Escribe cuantos números quieres sumar: "))
resultado_sum=[]
for i in range(cuantos_sum):
    num_sum=int(input("Ingrese el número de la suma: "))
    resultado_sum.append(str(num_sum))
resultado_sum=sum(str(resultado_sum))
return "El resultado de la suma es: " + str(suma)