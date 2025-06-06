CREATE TABLE "adocato_gato" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
"nome" varchar(100) NOT NULL, 
"sexo" varchar(1) NOT NULL, 
"cor" varchar(50) NOT NULL, 
"dataNascimento" date NOT NULL, 
"descricao" text NULL, 
"disponivel" bool NOT NULL, 
"raca_id" bigint NOT NULL REFERENCES "adocato_raca" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE INDEX "adocato_gato_raca_id_ae5eeaf1" ON "adocato_gato" ("raca_id");