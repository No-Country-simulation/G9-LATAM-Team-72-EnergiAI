package com.team72.energiai.api.dto;

public class AnalisisResponse {

    private String categoria;
    private Double costoEstimadoMensual;
    private String recomendacion;

    public String getCategoria() {
        return categoria;
    }

    public void setCategoria(String categoria) {
        this.categoria = categoria;
    }

    public Double getCostoEstimadoMensual() {
        return costoEstimadoMensual;
    }

    public void setCostoEstimadoMensual(Double costoEstimadoMensual) {
        this.costoEstimadoMensual = costoEstimadoMensual;
    }

    public String getRecomendacion() {
        return recomendacion;
    }

    public void setRecomendacion(String recomendacion) {
        this.recomendacion = recomendacion;
    }
}