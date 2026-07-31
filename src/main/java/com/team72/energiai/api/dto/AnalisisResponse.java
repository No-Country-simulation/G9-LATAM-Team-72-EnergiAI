package com.team72.energiai.api.dto;

import lombok.Data;

import java.util.List;

@Data
public class AnalisisResponse {

    private String categoria;

    private Double probabilidad;

    private Double costoEstimadoMensual;

    private List<String> recomendaciones;

}