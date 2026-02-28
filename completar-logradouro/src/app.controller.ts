import { Controller, Get, Param } from '@nestjs/common';
import { AppService } from './app.service';
import { CepInformation } from './agents/cep-information';
import { FindCEPOpenAI } from './agents/find-cep-openai';
import { FindCEPGemini } from './agents/find-cep-gemini';

@Controller()
export class AppController {
  constructor(private readonly appService: AppService,
    private readonly findCEPOpenAI: FindCEPOpenAI,
    private readonly findCEPGemini: FindCEPGemini
  ) {}

  @Get()
  getHello(): string {
    return this.appService.getHello();
  }

  @Get("cep/:cep")
  async getCepInformation(@Param("cep") cep: string): Promise<CepInformation> {
    return await this.findCEPOpenAI.getCepInformation(cep);
  }

  @Get("cep-gemini/:cep")
  async getCepInformationGemini(@Param("cep") cep: string): Promise<CepInformation> {
    return await this.findCEPGemini.getCepInformation(cep);
  }
}
