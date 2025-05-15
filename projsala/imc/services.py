class IMCService:
    def calcular_imc(self,altura,peso):
        imc= peso/(altura*altura)
        if imc < 18.5:
            classificacao = 'Abaixo do peso'
        elif imc < 24.9:
            classificacao = 'Peso normal'
        elif imc < 29.9:
            classificacao = 'Sobrepeso'
        else:
            classificacao = 'Obesidade'
        dicionario_imc= {
            'imc': imc,
            'classificacao': classificacao,
            'altura': altura,
            'peso': peso,
        }
        return dicionario_imc