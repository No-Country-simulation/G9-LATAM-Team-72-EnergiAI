package com.team72.energiai.api.service;

import com.team72.energiai.api.dto.MLRequest;
import com.team72.energiai.api.dto.MLResponse;
import com.team72.energiai.api.exception.MLServiceException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.ResourceAccessException;
import org.springframework.web.client.RestClient;

@Service
public class MLService {

    private static final Logger logger =
            LoggerFactory.getLogger(MLService.class);

    private final RestClient restClient;

    public MLService(@Value("${ml.service.url}") String mlServiceUrl) {

        this.restClient = RestClient.builder()
                .baseUrl(mlServiceUrl)
                .build();
    }

    public MLResponse predict(MLRequest request) {

        logger.info("Enviando solicitud al Asistente Virtual de EnergiAI.");

        try {

            MLResponse response = restClient.post()
                    .uri("/predict")
                    .body(request)
                    .retrieve()
                    .body(MLResponse.class);

            logger.info("Respuesta recibida correctamente del Asistente Virtual.");

            return response;

        } catch (ResourceAccessException e) {

            logger.error(
                    "No fue posible establecer comunicación con el Asistente Virtual.",
                    e
            );

            throw new MLServiceException(
                    "Nuestro Asistente Virtual de EnergiAI no se encuentra disponible en este momento. Inténtalo nuevamente más tarde.",
                    e
            );
        }
    }
}