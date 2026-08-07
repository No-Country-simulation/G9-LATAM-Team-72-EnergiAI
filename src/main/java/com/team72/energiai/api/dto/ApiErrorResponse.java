package com.team72.energiai.api.dto;

import lombok.AllArgsConstructor;
import lombok.Data;

import java.time.LocalDateTime;
import java.util.Map;

/**
 * Representa la estructura estándar de las respuestas
 * de error generadas por la API de EnergiAI.
 */
@Data
@AllArgsConstructor
public class ApiErrorResponse {

    /**
     * Fecha y hora en la que ocurrió el error.
     */
    private LocalDateTime timestamp;

    /**
     * Código HTTP de la respuesta.
     */
    private Integer status;

    /**
     * Nombre del estado HTTP.
     */
    private String error;

    /**
     * Descripción del error.
     */
    private String message;

    /**
     * Ruta donde ocurrió el error.
     */
    private String path;

    /**
     * Lista de errores de validación cuando aplica.
     */
    private Map<String, String> errors;

}