package com.team72.energiai.api.dto;

import lombok.Data;

import java.util.List;

@Data
public class MLResponse {

    private String categoria;
    private Double probabilidad;
    private List<String> recomendaciones;
}
