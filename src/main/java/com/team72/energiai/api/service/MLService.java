package com.team72.energiai.api.service;

import com.team72.energiai.api.dto.MLRequest;
import com.team72.energiai.api.dto.MLResponse;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.ResourceAccessException;
import org.springframework.web.client.RestClient;

@Service
public class MLService {

    private final RestClient restClient;

    public MLService(@Value("${ml.service.url}") String mlServiceUrl) {

        this.restClient = RestClient.builder()
                .baseUrl(mlServiceUrl)
                .build();
    }

    public MLResponse predict(MLRequest request) {

        try {

            return restClient.post()
                    .uri("/predict")
                    .body(request)
                    .retrieve()
                    .body(MLResponse.class);

        } catch (ResourceAccessException e) {

            throw new RuntimeException(
                    "El servicio de Inteligencia Artificial no está disponible en este momento."
            );

        }
    }
}