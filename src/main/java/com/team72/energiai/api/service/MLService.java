package com.team72.energiai.api.service;

import com.team72.energiai.api.dto.MLRequest;
import com.team72.energiai.api.dto.MLResponse;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;

@Service
public class MLService {

    private final RestClient restClient;

    public MLService(@Value("${ml.service.url}") String mlServiceUrl) {
        this.restClient = RestClient.builder()
                .baseUrl(mlServiceUrl)
                .build();
    }

/*
  public MLService (RestClient.Builder builder,
                    @Value("$ml.service.url") String mlServiceUrl){
      this.restClient = builder
              .baseUrl(mlServiceUrl)
              .build();
  }
*/

    public MLResponse predict(MLRequest request) {
        return restClient.post()
                .uri("/predict")
                .body(request)
                .retrieve()
                .body(MLResponse.class);
    }

}
