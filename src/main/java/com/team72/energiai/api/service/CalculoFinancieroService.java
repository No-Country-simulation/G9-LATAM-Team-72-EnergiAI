package com.team72.energiai.api.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

@Service
public class CalculoFinancieroService {

    /**
     * Tarifa configurada desde application.properties
     */
    @Value("${energia.tarifa-usd}")
    private Double tarifaKwhUsd;

    /**
     * Calcula el costo mensual en dólares.
     */
    public Double calcularCostoMensualUSD(Double consumoKwh) {

        if (consumoKwh == null) {
            return 0.0;
        }

        Double costo = consumoKwh * tarifaKwhUsd;

        return redondear(costo);
    }

    /**
     * Convierte el costo en USD a moneda local.
     */
    public Double calcularCostoMonedaLocal(Double costoUsd,
                                           Double tasaCambio) {

        if (costoUsd == null || tasaCambio == null) {
            return 0.0;
        }

        Double costoLocal = costoUsd * tasaCambio;

        return redondear(costoLocal);
    }

    /**
     * Redondea cualquier valor a dos decimales.
     */
    private Double redondear(Double valor) {

        return Math.round(valor * 100.0) / 100.0;

    }

}