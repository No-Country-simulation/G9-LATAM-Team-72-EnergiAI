package com.team72.energiai.api.service;

import com.team72.energiai.api.dto.AnalisisRequest;
import com.team72.energiai.api.dto.AnalisisResponse;
import org.springframework.stereotype.Service;

@Service
public class AnalisisEnergeticoService {

    public String obtenerEstado() {
        return "Servicio EnergiAI activo";
    }

    public AnalisisResponse analizar(AnalisisRequest request) {

        AnalisisResponse response = new AnalisisResponse();

        // Respuesta simulada (Mock) para Sprint 1
        response.setCategoria("Moderado");
        response.setCostoEstimadoMensual(315.00);
        response.setRecomendacion("Reducir el consumo durante las horas de mayor demanda.");

        return response;
    }
}