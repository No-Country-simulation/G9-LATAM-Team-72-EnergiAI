package com.team72.energiai.api.config;

import io.swagger.v3.oas.models.ExternalDocumentation;
import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Contact;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.info.License;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class OpenApiConfig {

    @Bean
    public OpenAPI energiaiOpenAPI() {

        return new OpenAPI()

                .info(
                        new Info()

                                .title("EnergiAI API")

                                .description("""
                                        API REST desarrollada para el Hackathon ONE | Oracle Next Education + Alura.

                                        EnergiAI permite analizar el consumo energético de hogares y comercios mediante un Asistente Virtual, generando recomendaciones inteligentes para promover la eficiencia energética y apoyar la toma de decisiones.
                                        """)

                                .version("1.0.0")

                                .contact(
                                        new Contact()

                                                .name("Team 72 - EnergiAI")
                                                .email("team72@energiai.com")
                                )

                                .license(
                                        new License()

                                                .name("Apache 2.0")
                                )
                )

                .externalDocs(

                        new ExternalDocumentation()

                                .description("Repositorio oficial del proyecto")
                                .url("https://github.com/No-Country-simulation/G9-LATAM-Team-72-EnergiAI")
                );
    }

}