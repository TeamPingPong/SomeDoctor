'use client'

import { useState } from 'react'
import { Radar } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
} from 'chart.js'
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

ChartJS.register(
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
)

type CategoryDescriptions = {
  [key: string]: string;
}

export default function ResultsPage() {
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null)
  
  // 이 데이터는 실제로는 서버에서 분석 결과를 받아와야 합니다
  const analysisData = {
    yourScore: 75,
    partnerScore: 80,
    finalScore: 78,
    finalScoreDescription: "전반적으로 긍정적인 대화를 나누셨습니다. 서로를 이해하려는 노력이 보입니다.",
    radarData: {
      labels: ['공감', '경청', '명확성', '긍정성', '개방성'],
      datasets: [
        {
          label: '대화 분석',
          data: [65, 70, 80, 75, 85],
          backgroundColor: 'rgba(255, 99, 132, 0.2)',
          borderColor: 'rgba(255, 99, 132, 1)',
          borderWidth: 1,
        },
      ],
    },
    categoryDescriptions: {
      '공감': '상대방의 감정을 이해하고 공감하는 능력이 있습니다.',
      '경청': '상대방의 말을 주의 깊게 듣고 있습니다.',
      '명확성': '의사 전달이 명확하고 이해하기 쉽습니다.',
      '긍정성': '대화에 긍정적인 태도를 보입니다.',
      '개방성': '새로운 아이디어와 의견을 수용하는 자세가 보입니다.',
    } as CategoryDescriptions,
    advice: "서로의 의견을 존중하면서 더 깊이 있는 대화를 나누어 보세요. 상대방의 감정에 더 주의를 기울이고, 적절한 질문을 통해 대화를 발전시켜 나가는 것이 좋겠습니다."
  }

  return (
    <div className="container mx-auto mt-10 space-y-8">
      <Card>
        <CardHeader>
          <CardTitle className="text-center">채팅 분석 결과</CardTitle>
        </CardHeader>
        <CardContent className="flex justify-between items-center">
          <div className="text-center">
            <p className="text-2xl font-bold">{analysisData.yourScore}</p>
            <p>나의 점수</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold">{analysisData.partnerScore}</p>
            <p>상대방의 점수</p>
          </div>
        </CardContent>
      </Card>
      <Card>
        <CardContent>
          <p className="text-xl font-bold mb-2">최종 점수: {analysisData.finalScore}</p>
          <p>{analysisData.finalScoreDescription}</p>
        </CardContent>
      </Card>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <Card>
          <CardContent>
            <Radar data={analysisData.radarData} />
          </CardContent>
        </Card>
        <Card>
          <CardContent>
            <h3 className="text-lg font-semibold mb-4">카테고리 설명</h3>
            {selectedCategory ? (
              <p>{analysisData.categoryDescriptions[selectedCategory]}</p>
            ) : (
              <p>차트에서 카테고리를 선택하세요.</p>
            )}
          </CardContent>
        </Card>
      </div>
      <Card>
        <CardHeader>
          <CardTitle>전체적인 대화에 대한 조언</CardTitle>
        </CardHeader>
        <CardContent>
          <p>{analysisData.advice}</p>
        </CardContent>
      </Card>
    </div>
  )
}