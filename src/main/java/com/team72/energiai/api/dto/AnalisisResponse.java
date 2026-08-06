package com.team72.energiai.api.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

import java.util.List;

@Data
@Schema(description = "Resultado del análisis energético realizado por EnergiAI.")
public class AnalisisResponse {

    @Schema(
            description = "Clasificación obtenida por el modelo de Machine Learning.",
            example = "Consumo Alto"
    )
    private String categoria;

    @Schema(
            description = "Probabilidad asociada a la clasificación.",
            example = "0.93"
    )
    private Double probabilidad;

    @Schema(
            description = "Costo mensual estimado del consumo energético en dólares (USD).",
            example = "262.50"
    )
    private Double costoEstimadoMensual;

    @Schema(
            description = "Lista de recomendaciones generadas por el Asistente Virtual de EnergiAI."
    )
    private List<String> recomendaciones;

}