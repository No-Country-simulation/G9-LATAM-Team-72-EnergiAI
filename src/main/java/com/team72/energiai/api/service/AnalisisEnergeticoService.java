package com.team72.energiai.api.service;

import com.team72.energiai.api.dto.AnalisisRequest;
import com.team72.energiai.api.dto.AnalisisResponse;
import com.team72.energiai.api.dto.MLRequest;
import com.team72.energiai.api.dto.MLResponse;
import org.springframework.stereotype.Service;

@Service
public class AnalisisEnergeticoService {

    private final MLService mlService;

    public AnalisisEnergeticoService(MLService mlService) {

        this.mlService = mlService;
    }

    public String obtenerEstado() {

        return "Servicio EnergiAI activo";
    }

    public AnalisisResponse analizar(AnalisisRequest request) {
        //crear la peticion para FastAPI
        MLRequest mlRequest = new MLRequest();

        mlRequest.setConsumoKwh(request.getConsumoKwh());
        mlRequest.setUsoHorarioPico(request.getUsoHorarioPico());
        mlRequest.setCantidadEquipos(request.getCantidadEquipos());
        mlRequest.setTipoInmueble(request.getTipoInmueble());
        mlRequest.setHorasAltoConsumo(request.getHorasAltoConsumo());

        //llamar al servicio de ML
        MLResponse mlResponse = mlService.predict(mlRequest);

        //construir la respuesta del backend
        AnalisisResponse response = new AnalisisResponse();

        response.setCategoria(mlResponse.getCategoria());
        response.setProbabilidad(mlResponse.getProbabilidad());
        response.setRecomendaciones(mlResponse.getRecomendaciones());

        return response;
/*
        // Respuesta simulada (Mock) para Sprint 1
        response.setCategoria("Moderado");
        response.setCostoEstimadoMensual(315.00);
        response.setRecomendacion("Reducir el consumo durante las horas de mayor demanda.");
 */
    }
}