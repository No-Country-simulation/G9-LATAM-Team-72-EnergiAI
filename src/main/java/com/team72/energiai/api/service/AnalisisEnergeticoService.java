package com.team72.energiai.api.service;

import com.team72.energiai.api.dto.AnalisisRequest;
import com.team72.energiai.api.dto.AnalisisResponse;
import com.team72.energiai.api.dto.MLRequest;
import com.team72.energiai.api.dto.MLResponse;
import org.springframework.stereotype.Service;

@Service
public class AnalisisEnergeticoService {

    private final MLService mlService;
    private final CalculoFinancieroService calculoFinancieroService;

    public AnalisisEnergeticoService(
            MLService mlService,
            CalculoFinancieroService calculoFinancieroService) {

        this.mlService = mlService;
        this.calculoFinancieroService = calculoFinancieroService;
    }

    public String obtenerEstado() {
        return "Servicio EnergiAI activo";
    }

    public AnalisisResponse analizar(AnalisisRequest request) {

        // Crear petición para FastAPI
        MLRequest mlRequest = new MLRequest();

        mlRequest.setConsumoKwh(request.getConsumoKwh());
        mlRequest.setUsoHorarioPico(request.getUsoHorarioPico());
        mlRequest.setCantidadEquipos(request.getCantidadEquipos());
        mlRequest.setTipoInmueble(request.getTipoInmueble());
        mlRequest.setHorasAltoConsumo(request.getHorasAltoConsumo());

        //valor por defecto para validaciones (Superficie en m2, requerido/relevante para Comercio)
        if (request.getSuperficieM2() == null){
            request.setSuperficieM2(0.0);
        }
        mlRequest.setSuperficieM2(request.getSuperficieM2());

        // Llamar al modelo de Machine Learning
        MLResponse mlResponse = mlService.predict(mlRequest);

        // Calcular costo mensual en USD
        Double costoMensual = calculoFinancieroService.calcularCostoMensualUSD(
                request.getConsumoKwh()
        );

        // Construir respuesta
        AnalisisResponse response = new AnalisisResponse();

        response.setCategoria(mlResponse.getCategoria());
        response.setProbabilidad(mlResponse.getProbabilidad());
        response.setCostoEstimadoMensual(costoMensual);
        response.setRecomendaciones(mlResponse.getRecomendaciones());

        return response;
    }
}