# modules/metadados.py

metadados_blocos = {
    "1. Sociodemográfico": {
        "tipo": "sociodemografico",
        "tipos_personalizados": {
            "Qual é o seu gênero?": ["","Masculinho", "Feminino", "Não-binário", "Outros"],
            "Quantos anos você tem?": "numero",
            "Você mora em qual região do país?": ["","Norte","Nordeste","Sul","Sudeste","Centro-Oeste"],
            "Qual é a renda do seu núcleo familiar, em relação ao salário mínimo?": [
                "",
                "Menos de 1 salário mínimo (Menos de R$ 1.518,00)",
                "De 1 a 2 salários mínimos (R$ 1.518,00 a R$ 3.036,00)",
                "De 2 a 3 salários mínimos (R$ 3.036,01 a R$ 4.554,00)",
                "De 3 a 5 salários mínimos (R$ 4.554,01 a R$ 7.590,00)",
                "De 5 a 10 salários mínimos (R$ 7.590,01 a R$ 15.180,00)",
                "Acima de 10 salários mínimos (Mais de R$ 15.180,00)",
            ],
            "Qual é o seu nível de escolaridade?": [
                "",
                "Ensino Superior Incompleto",
                "Ensino Superior Completo",
                "Mestrado",
                "Doutorado",
            ],
            "Quantos filhos você tem?": [
                "",
                "Não tenho filhos.",
                "1",
                "2",
                "3 ou mais",
            ],
        }
    },
    "2. LPFS-BF": {
        "tipo": "likert",
        "escala": (1, 4),
        "labels": ("1 - Nada verdadeiro", "4 - Totalmente verdadeiro"),
    },
    "3. FFMQ-BR": {
        "tipo": "likert",
        "escala": (1, 5),
        "labels": ("1 - Nunca ou muito raramente verdadeiro", "5 - Muito frequentemente verdadeiro"),
    },
    "4. PID-5-BF": {
        "tipo": "likert",
        "escala": (0, 3),
        "labels": ("0 - Falso ou muito falso", "3 - Verdadeiro ou muito verdadeiro"),
    },
    "5. AQ-50": {
        "tipo": "likert",
        "escala": (1, 4),
        "labels": ("1 - Discordo totalmente", "4 - Concordo totalmente"),
    },
}
