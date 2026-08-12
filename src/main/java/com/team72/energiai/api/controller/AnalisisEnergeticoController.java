package com.team72.energiai.api.controller;

import com.team72.energiai.api.dto.AnalisisRequest;
import com.team72.energiai.api.dto.AnalisisResponse;
import com.team72.energiai.api.dto.ApiErrorResponse;
import com.team72.energiai.api.service.AnalisisEnergeticoService;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;

import jakarta.validation.Valid;

import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api")
@Tag(
        name = "Análisis Energético",
        description = "Endpoints para interactuar con el Asistente Virtual de EnergiAI y realizar análisis del consumo energético."
)
public class AnalisisEnergeticoController {

    private final AnalisisEnergeticoService service;

    public AnalisisEnergeticoController(
            AnalisisEnergeticoService service) {

        this.service = service;
    }

    @Operation(
            summary = "Consultar el estado del servicio",
            description = "Verifica que la API de EnergiAI se encuentre disponible."
    )
    @ApiResponses({
            @ApiResponse(
                    responseCode = "200",
                    description = "Servicio disponible"
            )
    })
    @GetMapping("/")
    public ResponseEntity<String> inicio() {

        return ResponseEntity.ok(
                service.obtenerEstado()
        );
    }

    @Operation(
            summary = "Realizar un análisis energético",
            description = """
                    Recibe la información de consumo energético de un hogar o comercio,
                    consulta el Asistente Virtual de EnergiAI y devuelve la clasificación
                    del consumo, el costo mensual estimado y las recomendaciones generadas.
                    """
    )
    @ApiResponses({
            @ApiResponse(
                    responseCode = "200",
                    description = "Análisis realizado correctamente"
            ),
            @ApiResponse(
                    responseCode = "400",
                    description = "Los datos enviados no son válidos",
                    content = @Content(
                            mediaType = MediaType.APPLICATION_JSON_VALUE,
                            schema = @Schema(implementation = ApiErrorResponse.class)
                    )
            ),
            @ApiResponse(
                    responseCode = "500",
                    description = "Se produjo un error interno inesperado en el servidor",
                    content = @Content(
                            mediaType = MediaType.APPLICATION_JSON_VALUE,
                            schema = @Schema(implementation = ApiErrorResponse.class)
                    )
            ),
            @ApiResponse(
                    responseCode = "503",
                    description = "El Asistente Virtual de EnergiAI no se encuentra disponible",
                    content = @Content(
                            mediaType = MediaType.APPLICATION_JSON_VALUE,
                            schema = @Schema(implementation = ApiErrorResponse.class)
                    )
            )
    })
    @PostMapping("/analisis-energetico")
    public ResponseEntity<AnalisisResponse> analizar(
            @Valid @RequestBody AnalisisRequest request) {

        AnalisisResponse response = service.analizar(request);

        return ResponseEntity.ok(response);
    }

}