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
  Legend
} from 'chart.js'
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { useResultStore } from '@/store/resultStore'

ChartJS.register(
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
)

export default function Results() {
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null)
  const result = useResultStore((state) => state.result)
  // 이 데이터는 실제로는 서버에서 분석 결과를 받아와야 합니다
  const analysisData = {
    participants: [
      { name: '나', score: 75 },
      { name: '참여자 1', score: 80 },
      { name: '참여자 2', score: 70 },
      { name: '참여자 3', score: 85 },
    ],
    finalScore: 78,
    finalScoreDescription: "전반적으로 긍정적인 대화를 나누셨습니다. 서로를 이해하려는 노력이 보입니다.",
    radarData: {
      labels: ['경계 지수', '애정 지수', '친밀 지수', '대화 흐름 지수', '상호존중 및 공감 지수', '호기심 지수', '유머 지수'],
      datasets: [
        {
          label: '대화 분석',
          data: [65, 70, 80, 75, 85, 60, 72],
          backgroundColor: 'rgba(255, 99, 132, 0.2)',
          borderColor: 'rgba(255, 99, 132, 1)',
          borderWidth: 1,
        },
      ],
    },
    categoryDescriptions: {
      '경계 지수': '상대방과의 대화에서 적절한 경계를 유지하고 있습니다. 개인적인 공간과 존중을 잘 지키고 있어요.',
      '애정 지수': '상대방에 대한 애정과 관심을 잘 표현하고 있습니다. 따뜻한 말과 행동이 대화에 잘 녹아있어요.',
      '친밀 지수': '상대방과 편안하고 가까운 관계를 유지하고 있습니다. 서로를 잘 이해하고 있는 것 같아요.',
      '대화 흐름 지수': '대화가 자연스럽게 흘러가고 있습니다. 주제 전환이 매끄럽고 대화가 끊기지 않아요.',
      '상호존중 및 공감 지수': '서로의 의견을 존중하고 감정에 공감하고 있습니다. 상대방의 입장을 잘 이해하려 노력하고 있어요.',
      '호기심 지수': '상대방에 대해 관심을 가지고 새로운 것을 알아가려는 태도가 보입니다. 다양한 주제에 대해 호기심을 보이고 있어요.',
      '유머 지수': '대화에 적절한 유머를 사용하고 있습니다. 웃음을 통해 대화의 분위기를 밝게 만들고 있어요.',
    },
    advice: "서로의 의견을 존중하면서 더 깊이 있는 대화를 나누어 보세요. 상대방의 감정에 더 주의를 기울이고, 적절한 질문을 통해 대화를 발전시켜 나가는 것이 좋겠습니다."
  }

  const handleCategoryClick = (category: string) => {
    setSelectedCategory(category)
  }

  return (
    <div className="container mx-auto mt-10 space-y-8">
      <Card>
        <CardHeader>
          <CardTitle className="text-center">채팅 분석 결과</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap justify-around items-center">
            {analysisData.participants.map((participant, index) => (
              <div key={index} className="text-center p-4">
                <p className="text-2xl font-bold">{participant.score}</p>
                <p>{participant.name}</p>
              </div>
            ))}
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
            <Radar 
              data={analysisData.radarData} 
              options={{
                onClick: (event, elements) => {
                  if (elements.length > 0) {
                    const index = elements[0].index
                    handleCategoryClick(analysisData.radarData.labels[index])
                  }
                },
                plugins: {
                  tooltip: {
                    callbacks: {
                      label: (context) => {
                        return `${context.label}: ${context.formattedValue}`
                      }
                    }
                  }
                },
                scales: {
                  r: {
                    min: 0,
                    max: 100,
                    ticks: {
                      stepSize: 20
                    }
                  }
                }
              }}
            />
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>{selectedCategory || '카테고리 설명'}</CardTitle>
          </CardHeader>
          <CardContent>
            {selectedCategory ? (
              // <p>{analysisData.categoryDescriptions[selectedCategory]}</p>
              <p>{analysisData.categoryDescriptions[selectedCategory as keyof typeof analysisData.categoryDescriptions]}</p>
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