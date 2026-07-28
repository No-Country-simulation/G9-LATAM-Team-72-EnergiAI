package com.team72.energiai.api.service;

import org.springframework.stereotype.Service;

@Service
public class CalculoFinancieroService {

    /**
     * Tarifa base definida por el proyecto.
     * 0.75 USD por cada kWh consumido.
     */
    private static final double TARIFA_KWH_USD = 0.75;

    /**
     * Calcula el costo mensual en dólares.
     *
     * Fórmula:
     * consumo mensual × tarifa USD
     */
    public Double calcularCostoMensualUSD(Double consumoKwh) {

        if (consumoKwh == null) {
            return 0.0;
        }

        return consumoKwh * TARIFA_KWH_USD;
    }

    /**
     * Convierte el costo en USD a moneda local.
     *
     * Fórmula:
     * costo USD × tasa de cambio
     */
    public Double calcularCostoMonedaLocal(Double costoUsd,
                                           Double tasaCambio) {

        if (costoUsd == null || tasaCambio == null) {
            return 0.0;
        }

        return costoUsd * tasaCambio;
    }

}