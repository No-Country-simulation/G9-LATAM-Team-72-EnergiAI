package com.team72.energiai.api.service;

import com.team72.energiai.api.dto.AnalisisRequest;
import com.team72.energiai.api.dto.AnalisisResponse;
import com.team72.energiai.api.dto.MLRequest;
import com.team72.energiai.api.dto.MLResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

@Service
public class AnalisisEnergeticoService {

    private static final Logger logger =
            LoggerFactory.getLogger(AnalisisEnergeticoService.class);

    private final MLService mlService;
    private final CalculoFinancieroService calculoFinancieroService;

    public AnalisisEnergeticoService(
            MLService mlService,
            CalculoFinancieroService calculoFinancieroService) {

        this.mlService = mlService;
        this.calculoFinancieroService = calculoFinancieroService;
    }

    /**
     * Verifica que el Asistente Virtual de EnergiAI se encuentre disponible.
     */
    public String obtenerEstado() {
        return "Asistente Virtual de EnergiAI disponible.";
    }

    /**
     * Realiza el análisis energético utilizando el Asistente Virtual de EnergiAI.
     */
    public AnalisisResponse analizar(AnalisisRequest request) {

        logger.info(
                "Iniciando análisis energético para tipo de inmueble: {}",
                request.getTipoInmueble()
        );

        // Construcción de la solicitud para el servicio de IA
        MLRequest mlRequest = new MLRequest();

        mlRequest.setConsumoKwh(request.getConsumoKwh());
        mlRequest.setUsoHorarioPico(request.getUsoHorarioPico());
        mlRequest.setCantidadEquipos(request.getCantidadEquipos());
        mlRequest.setTipoInmueble(request.getTipoInmueble());
        mlRequest.setHorasAltoConsumo(request.getHorasAltoConsumo());

        // Valor por defecto cuando no se envía la superficie
        mlRequest.setSuperficieM2(
                request.getSuperficieM2() != null
                        ? request.getSuperficieM2()
                        : 0.0
        );

        logger.info("Consultando el Asistente Virtual de EnergiAI.");

        // Obtener predicción desde FastAPI
        MLResponse mlResponse = mlService.predict(mlRequest);

        logger.info(
                "Resultado del análisis -> Categoría: {} | Confianza: {}",
                mlResponse.getCategoria(),
                mlResponse.getProbabilidad()
        );

        // Calcular el costo estimado mensual
        Double costoMensual =
                calculoFinancieroService.calcularCostoMensualUSD(
                        request.getConsumoKwh()
                );

        // Construir la respuesta para el cliente
        AnalisisResponse response = new AnalisisResponse();

        response.setCategoria(mlResponse.getCategoria());
        response.setProbabilidad(mlResponse.getProbabilidad());
        response.setCostoEstimadoMensual(costoMensual);
        response.setRecomendaciones(mlResponse.getRecomendaciones());

        logger.info("Análisis energético completado exitosamente.");

        return response;
    }
}