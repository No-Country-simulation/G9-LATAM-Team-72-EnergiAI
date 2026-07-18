package com.team72.energiai.api.controller;

import com.team72.energiai.api.dto.AnalisisRequest;
import com.team72.energiai.api.dto.AnalisisResponse;
import com.team72.energiai.api.service.AnalisisEnergeticoService;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api")
public class AnalisisEnergeticoController {

    private final AnalisisEnergeticoService service;

    public AnalisisEnergeticoController(AnalisisEnergeticoService service) {
        this.service = service;
    }

    /**
     * Endpoint para verificar que la API está funcionando.
     */
    @GetMapping("/")
    public String inicio() {
        return service.obtenerEstado();
    }

    /**
     * Endpoint principal del proyecto.
     * Recibe los datos de consumo energético y devuelve un análisis.
     */
    @PostMapping("/analisis-energetico")
    public AnalisisResponse analizar(@Valid @RequestBody AnalisisRequest request) {
        return service.analizar(request);
    }

}