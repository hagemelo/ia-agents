import { Controller, Get, Param } from '@nestjs/common';
import { AppService } from './app.service';
import { CepInformation } from './agents/cep-information';
import { FindCEPOpenAI } from './agents/find-cep-openai';

@Controller()
export class AppController {
  constructor(private readonly appService: AppService,
    private readonly findCEPOpenAI: FindCEPOpenAI
  ) {}

  @Get()
  getHello(): string {
    return this.appService.getHello();
  }

  @Get("cep/:cep")
  async getCepInformation(@Param("cep") cep: string): Promise<CepInformation> {
    return await this.findCEPOpenAI.getCepInformation(cep);
  }
}
